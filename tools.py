# tools.py - GPT-Image-1 Image Generation Tools

import os
import base64
from datetime import datetime
from openai import OpenAI
from dotenv import dotenv_values

# Load environment variables
config = dotenv_values(".env")

def generate_image(
    prompt: str,
    background: str = "auto",
    model: str = "gpt-image-1", 
    moderation: str = "low",
    n: int = 1,
    output_compression: int = 85,
    output_format: str = "jpeg",
    quality: str = "medium",
    size: str = "auto"
) -> tuple[list, str]:
    """
    Generate images from text prompts using OpenAI's GPT-Image-1 model.
    
    Creates high-quality images from detailed text descriptions with full control over
    output parameters including quality, size, format, and background transparency.
    
    Args:
        prompt (str): Detailed description of the image to generate (max 32,000 characters).
                     Be specific about style, composition, lighting, and details for best results.
        background (str): Background transparency control. Options:
                         - "auto": AI decides best background (default)
                         - "transparent": Creates transparent background (PNG/WebP only)
                         - "opaque": Forces solid background
        model (str): Image generation model to use (default: "gpt-image-1")
        moderation (str): Content filtering level. Options:
                         - "low": Less restrictive filtering for artistic content
                         - "auto": Standard content filtering
        n (int): Number of images to generate (1-10, default: 1)
        output_compression (int): Compression level for JPEG/WebP (0-100%, default: 85)
        output_format (str): Image file format. Options:
                            - "jpeg": Smaller files, good for photos
                            - "png": Lossless, supports transparency  
                            - "webp": Modern format, good compression
        quality (str): Image quality level. Options:
                      - "auto": AI selects optimal quality
                      - "low": Fast generation, lower cost
                      - "medium": Balanced quality and cost (recommended)
                      - "high": Maximum quality, higher cost
        size (str): Image dimensions. Options:
                   - "auto": AI selects optimal size
                   - "1024x1024": Square format
                   - "1536x1024": Landscape format
                   - "1024x1536": Portrait format
    
    Returns:
        tuple[list, str]: (list_of_image_file_paths, detailed_generation_info_markdown)
                         Returns ([], error_message) if generation fails.
    
    Example:
        image_paths, info = generate_image(
            prompt="A serene mountain lake at sunset with reflections",
            quality="high",
            size="1536x1024",
            output_format="png"
        )
    """
    try:
        # Validate inputs
        if not prompt.strip():
            return [], "❌ **Error:** Prompt cannot be empty."
        
        api_key = config.get("OPENAI_API_KEY")
        if not api_key:
            return [], "❌ **Error:** OpenAI API key not found in environment variables."
        
        client = OpenAI(api_key=api_key)
        
        # Generate image using OpenAI API
        response = client.images.generate(
            model=model,
            prompt=prompt,
            background=background,
            moderation=moderation,
            n=n,
            output_compression=output_compression,
            output_format=output_format,
            quality=quality,
            size=size
        )
        
        # Extract response data
        created_timestamp = response.created
        usage = response.usage
        
        # Save all generated images
        os.makedirs("generated_images", exist_ok=True)
        extension = "jpg" if output_format == "jpeg" else output_format
        image_paths = []
        
        for i, image_data in enumerate(response.data):
            # Create filename for each image
            filename = f"generated_{created_timestamp}_{i+1}.{extension}"
            filepath = os.path.join("generated_images", filename)
            
            # Decode and save image
            image_bytes = base64.b64decode(image_data.b64_json)
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            
            image_paths.append(filepath)
        
        # Calculate costs
        text_tokens = usage.input_tokens_details.text_tokens
        image_tokens = usage.input_tokens_details.image_tokens
        
        input_cost = (text_tokens / 1_000_000) * 5.00  # Text tokens
        output_cost = (usage.output_tokens / 1_000_000) * 40.00  # Image tokens
        total_cost = input_cost + output_cost
        
        # Generate info
        generation_info = f"""## ✅ Images Generated Successfully!

### 📊 Generation Details
- **Model:** {model}
- **Images Created:** {len(image_paths)}
- **Quality:** {quality}
- **Size:** {size} 
- **Format:** {output_format.upper()}
- **Background:** {background}
- **Compression:** {output_compression}%
- **Created:** {datetime.fromtimestamp(created_timestamp).strftime('%Y-%m-%d %H:%M:%S')}

### 🔢 Token Usage
- **Text Tokens:** {text_tokens:,}
- **Image Tokens:** {image_tokens:,}
- **Output Tokens:** {usage.output_tokens:,}
- **Total Tokens:** {usage.total_tokens:,}

### 💰 Cost Breakdown
- **Input Cost:** ${input_cost:.4f}
- **Output Cost:** ${output_cost:.4f}
- **Total Cost:** ${total_cost:.4f}
- **Cost per Image:** ${total_cost/len(image_paths):.4f}

### 📝 Prompt
"{prompt[:300]}{'...' if len(prompt) > 300 else ''}"
"""
        
        return image_paths, generation_info
        
    except Exception as e:
        error_info = f"""## ❌ Generation Failed

**Error:** {str(e)}

**Troubleshooting:**
- Verify OpenAI API key is valid
- Check prompt length (max 32,000 characters)
- Ensure sufficient API credits
- Try different quality/size settings
"""
        return [], error_info

def edit_image(
    image_files,  # File input(s)
    prompt: str,
    background: str = "auto",
    mask_file = None,
    model: str = "gpt-image-1",
    n: int = 1, 
    quality: str = "medium",
    size: str = "auto"
) -> tuple[list, str]:
    """
    Edit, modify, or combine existing images using text instructions with GPT-Image-1.
    
    Transform existing images by providing detailed text instructions. Can combine multiple
    images, apply masks for targeted editing, and modify specific aspects while preserving
    overall composition.
    
    Args:
        image_files: Single uploaded image file or list of image files to edit/combine.
                    Supports PNG, JPEG, WebP formats. Max 50MB per image, up to 16 images total.
        prompt (str): Detailed instructions for editing or combining the images (max 32,000 chars).
                     Describe the entire desired result, not just the changes.
                     Example: "Combine the cat and hat to show the cat wearing the hat in a garden"
        background (str): Background handling for edited image. Options:
                         - "auto": AI determines best background treatment
                         - "transparent": Create transparent background (PNG/WebP output)
                         - "opaque": Ensure solid background
        mask_file: Optional mask image file for targeted editing. White areas indicate regions
                  to edit, black areas to preserve. Must have alpha channel and match first
                  image dimensions. Applied only to the first image if multiple images provided.
        model (str): Model to use for editing (default: "gpt-image-1")
        n (int): Number of edited variations to generate (1-10, default: 1)
        quality (str): Output quality level. Options:
                      - "auto": Optimal quality selection
                      - "low": Faster processing, lower cost
                      - "medium": Balanced quality and speed (recommended)
                      - "high": Maximum quality, slower processing
        size (str): Output image dimensions. Options:
                   - "auto": Maintains input proportions or optimizes
                   - "1024x1024": Square output
                   - "1536x1024": Landscape output  
                   - "1024x1536": Portrait output
    
    Returns:
        tuple[list, str]: (list_of_edited_image_paths, detailed_edit_info_markdown)
                         Returns ([], error_message) if editing fails.
    
    Example:
        edited_paths, info = edit_image(
            image_files=uploaded_image,
            prompt="Add a rainbow in the sky and make it sunset lighting",
            quality="high",
            background="opaque"
        )
    """
    try:
        # Validate inputs
        if image_files is None:
            return [], "❌ **Error:** Please upload at least one image file."
        
        if not prompt.strip():
            return [], "❌ **Error:** Edit prompt cannot be empty."
        
        api_key = config.get("OPENAI_API_KEY")
        if not api_key:
            return [], "❌ **Error:** OpenAI API key not found in environment variables."
        
        client = OpenAI(api_key=api_key)
        
        # Prepare image files
        if isinstance(image_files, str):
            # Single file
            images = [open(image_files, "rb")]
            image_count = 1
        else:
            # Multiple files
            images = [open(img_path, "rb") for img_path in image_files]
            image_count = len(images)
        
        # Prepare edit parameters
        edit_params = {
            "model": model,
            "image": images if image_count > 1 else images[0],
            "prompt": prompt,
            "background": background,
            "n": n,
            "quality": quality,
            "size": size
        }
        
        # Add mask if provided
        if mask_file:
            edit_params["mask"] = open(mask_file, "rb")
        
        # Edit image using OpenAI API
        response = client.images.edit(**edit_params)
        
        # Close file handles
        for img in images:
            img.close()
        if mask_file:
            edit_params["mask"].close()
        
        # Extract response data
        created_timestamp = response.created
        usage = response.usage
        
        # Save all edited images
        os.makedirs("generated_images", exist_ok=True)
        image_paths = []
        
        for i, image_data in enumerate(response.data):
            # Create filename for each edited image
            filename = f"edited_{created_timestamp}_{i+1}.png"
            filepath = os.path.join("generated_images", filename)
            
            # Decode and save image
            image_bytes = base64.b64decode(image_data.b64_json)
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            
            image_paths.append(filepath)
        
        # Calculate costs
        text_tokens = usage.input_tokens_details.text_tokens
        image_tokens = usage.input_tokens_details.image_tokens
        
        input_cost = (text_tokens / 1_000_000) * 5.00 + (image_tokens / 1_000_000) * 10.00
        output_cost = (usage.output_tokens / 1_000_000) * 40.00
        total_cost = input_cost + output_cost
        
        # Generate info
        edit_info = f"""## ✅ Images Edited Successfully!

### 📊 Edit Details
- **Model:** {model}
- **Input Images:** {image_count}
- **Output Images:** {len(image_paths)}
- **Quality:** {quality}
- **Size:** {size}
- **Background:** {background}
- **Mask Applied:** {"Yes" if mask_file else "No"}
- **Created:** {datetime.fromtimestamp(created_timestamp).strftime('%Y-%m-%d %H:%M:%S')}

### 🔢 Token Usage
- **Text Tokens:** {text_tokens:,}
- **Input Image Tokens:** {image_tokens:,}
- **Output Tokens:** {usage.output_tokens:,}
- **Total Tokens:** {usage.total_tokens:,}

### 💰 Cost Breakdown
- **Input Cost:** ${input_cost:.4f} (text + images)
- **Output Cost:** ${output_cost:.4f}
- **Total Cost:** ${total_cost:.4f}
- **Cost per Output Image:** ${total_cost/len(image_paths):.4f}

### 📝 Edit Instructions
"{prompt[:300]}{'...' if len(prompt) > 300 else ''}"
"""
        
        return image_paths, edit_info
        
    except Exception as e:
        error_info = f"""## ❌ Edit Failed

**Error:** {str(e)}

**Troubleshooting:**
- Ensure images are PNG, JPEG, or WebP format
- Check file sizes (max 50MB per image)
- Verify mask has alpha channel and matches image dimensions
- Try simpler edit instructions
- Reduce number of input images
"""
        return [], error_info