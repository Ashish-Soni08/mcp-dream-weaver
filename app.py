import gradio as gr
from resources import (
    get_about_info,
    get_setup_steps,
    get_model_overview,
    get_model_pricing,
    get_model_rate_limits
)
from tools import generate_image, edit_image

# Create clean tabbed interface
demo = gr.TabbedInterface(
    [
        # Image Generation Tool
        gr.Interface(
            fn=generate_image,
            inputs=[
                gr.Textbox(label="Prompt", placeholder="Describe the image you want to create in detail...", lines=4),
                gr.Dropdown(choices=["auto", "transparent", "opaque"], value="auto", label="Background"),
                gr.Dropdown(choices=["gpt-image-1"], value="gpt-image-1", label="Model"),
                gr.Dropdown(choices=["low", "auto"], value="low", label="Moderation"),
                gr.Slider(minimum=1, maximum=10, value=1, step=1, label="Number of Images"),
                gr.Slider(minimum=0, maximum=100, value=85, step=5, label="Output Compression %"),
                gr.Dropdown(choices=["jpeg", "png", "webp"], value="jpeg", label="Output Format"),
                gr.Dropdown(choices=["auto", "low", "medium", "high"], value="medium", label="Quality"),
                gr.Dropdown(
                    choices=["auto", "1024x1024", "1536x1024", "1024x1536"], 
                    value="auto", 
                    label="Size",
                    info="auto: AI selects best size | 1024x1024: Square (social media, avatars) | 1536x1024: Landscape (scenery, desktop) | 1024x1536: Portrait (people, mobile)"
                )
            ],
            outputs=[gr.Gallery(label="Generated Images", show_label=True, columns=2), gr.Markdown(label="Generation Info")],
            api_name="generate_image"
        ),
        
        # Image Editing Tool
        gr.Interface(
            fn=edit_image,
            inputs=[
                gr.File(label="Upload Image(s) to Edit", file_types=["image"]),
                gr.Textbox(label="Edit Instructions", placeholder="Describe the entire desired result, not just changes...", lines=4),
                gr.Dropdown(
                    choices=["auto", "transparent", "opaque"], 
                    value="auto", 
                    label="Background",
                    info="auto: AI decides | transparent: clear background | opaque: solid background"
                ),
                gr.File(label="Upload Mask (Optional)", file_types=["image"]),
                gr.Dropdown(choices=["gpt-image-1"], value="gpt-image-1", label="Model"),
                gr.Slider(minimum=1, maximum=10, value=1, step=1, label="Number of Images"),
                gr.Dropdown(
                    choices=["auto", "low", "medium", "high"], 
                    value="medium", 
                    label="Quality",
                    info="low: fast/cheap | medium: balanced | high: best quality/expensive"
                ),
                gr.Dropdown(
                    choices=["auto", "1024x1024", "1536x1024", "1024x1536"], 
                    value="auto", 
                    label="Size",
                    info="auto: AI selects best size | 1024x1024: Square (social media, avatars) | 1536x1024: Landscape (scenery, desktop) | 1024x1536: Portrait (people, mobile)"
                )
            ],
            outputs=[gr.Gallery(label="Edited Images", show_label=True, columns=2), gr.Markdown(label="Edit Info")],
            api_name="edit_image"
        ),
        
        # Documentation Tools  
        gr.Interface(get_about_info, None, "markdown", api_name="get_about_info"),
        gr.Interface(get_setup_steps, None, "markdown", api_name="get_setup_steps"),
        gr.Interface(get_model_overview, None, "markdown", api_name="get_model_overview"),
        gr.Interface(get_model_pricing, None, "markdown", api_name="get_model_pricing"),
        gr.Interface(get_model_rate_limits, None, "markdown", api_name="get_model_rate_limits"),
    ],
    [
        "🎨 Generate Images",
        "✏️ Edit Images", 
        "📖 About",
        "🔑 Setup Guide", 
        "🤖 Model Overview",
        "💰 Pricing",
        "⏱️ Rate Limits",
    ],
    title="🎨 Dream Weaver - OpenAI Image Generation MCP Server"
)

# Launch with MCP server enabled
if __name__ == "__main__":
    demo.launch(mcp_server=True)