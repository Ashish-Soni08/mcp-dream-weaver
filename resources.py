"""
Model documentation for GPT-Image-1.
Provides users with essential model information, pricing, and specifications.
"""


def get_about_info() -> str:
    """
    Information about the Dream Weaver MCP server and its origin story.
    """
    return """# About Dream Weaver MCP Server

## 🏆 Born from Innovation

This MCP server was created during the **Agents MCP Hackathon** hosted by Hugging Face!

🔗 **Hackathon**: https://huggingface.co/Agents-MCP-Hackathon

## 🎯 What is Dream Weaver?

Dream Weaver is an MCP (Model Context Protocol) server that **weaves your wildest prompts into stunning images** using OpenAI's state-of-the-art GPT-Image-1 model.

## ✨ Features

- **Image Generation**: Turn text prompts into beautiful images

## 🛠️ Built With

- **MCP (Model Context Protocol)**: Standardized AI context sharing
- **Python FastMCP**: Rapid MCP server development
- **OpenAI GPT-Image-1**: Latest image generation model
- ⭐ **Claude AI Assistant**: Built with guidance from Claude
- **Love for AI Innovation**: Created with passion during the hackathon

## 🎨 The Vision

Making AI image generation seamlessly accessible through the Model Context Protocol - enabling any MCP-compatible client to create stunning visuals with simple text prompts.

---

*Created with ❤️ during the Agents MCP Hackathon*
*Turning imagination into reality, one prompt at a time* ✨"""

def get_setup_steps() -> str:
    """
    Step-by-step guide to obtain an OpenAI API key for image generation.
    """
    return """# Getting Your OpenAI API Key

## Quick Setup (4 Steps)

### Step 1: Create OpenAI Account
- Visit https://platform.openai.com/signup
- Sign up with your email or use existing account
- Verify your email address

### Step 2: Navigate to API Keys
- Go to https://platform.openai.com/api-keys
- Click "Create new secret key"
- Give it a name (e.g., "Dream Weaver Image Generation")

### Step 3: Copy and Store Your Key
- **Copy the key immediately** (you won't see it again!)
- Add it to your `.env` file:
  ```
  OPENAI_API_KEY=sk-proj-your-key-here
  ```
- Keep it secure and never share it publicly

### Step 4: Complete Organization Verification (GPT-Image-1)
- Go to your OpenAI developer console
- Complete the **API Organization Verification** process
- This is required before using `gpt-image-1` model
- Verification ensures responsible use of the image generation model

## Important Notes
- ⚠️ **API keys are sensitive** - treat them like passwords
- 💳 **Billing required** - Add payment method for image generation
- 🔄 **Free tier doesn't support GPT-Image-1** - see pricing resource for costs
- ✅ **Verification required** - Complete organization verification for gpt-image-1

## Need Help?
- Check the model pricing: `get_model_pricing()`
- Review rate limits: `get_model_rate_limits()`

Ready to start generating images once your API key is set up! 🎨"""

def get_model_overview() -> str:
    """
    Overview of OpenAI's GPT-Image-1 model - what it is and what it can do.
    """
    return """# GPT-Image-1 Overview

## What is GPT-Image-1?
State-of-the-art image generation model. It is a natively multimodal language model that accepts both text and image inputs, and produces image outputs.

## Performance Characteristics
- **Performance**: Higher
- **Speed**: Slowest  
- **Price**: $5 • $40 (Input • Output)

## Input/Output
- **Input**: Text, image
- **Output**: Image

## Features
- ✅ **Inpainting**: Supported

## Model Snapshots
- **gpt-image-1**: Current version
- **gpt-image-1**: Alias for latest

## Official Documentation
For complete details: https://platform.openai.com/docs/models/gpt-image-1"""


def get_model_pricing() -> str:
    """
    Complete pricing breakdown for GPT-Image-1 model in easy-to-read tables.
    """
    return """# GPT-Image-1 Pricing

## Text Tokens (Per 1M tokens)
| Type | Price |
|------|-------|
| Input | $5.00 |
| Cached input | $1.25 |

## Image Tokens (Per 1M tokens)
| Type | Price |
|------|-------|
| Input | $10.00 |
| Cached input | $2.50 |
| Output | $40.00 |

## Image Generation (Per image)

### Low Quality
| Resolution | Price |
|------------|-------|
| 1024x1024 | $0.011 |
| 1024x1536 | $0.016 |
| 1536x1024 | $0.016 |

### Medium Quality  
| Resolution | Price |
|------------|-------|
| 1024x1024 | $0.042 |
| 1024x1536 | $0.063 |
| 1536x1024 | $0.063 |

### High Quality
| Resolution | Price |
|------------|-------|
| 1024x1024 | $0.167 |
| 1024x1536 | $0.25 |
| 1536x1024 | $0.25 |"""


def get_model_specifications() -> str:
    """
    Technical specifications and supported formats for GPT-Image-1.
    """
    return """# GPT-Image-1 Technical Specifications

## Modalities
- **Text**: Input only
- **Image**: Input and output  
- **Audio**: Not supported

## Supported Endpoints
- ✅ Chat Completions: `v1/chat/completions`
- ✅ Responses: `v1/responses`
- ✅ Realtime: `v1/realtime`
- ✅ Assistants: `v1/assistants`
- ✅ Batch: `v1/batch`
- ✅ Fine-tuning: `v1/fine-tuning`
- ✅ Embeddings: `v1/embeddings`
- ✅ **Image generation**: `v1/images/generations`
- ✅ **Image edit**: `v1/images/edits`
- ✅ Speech generation: `v1/audio/speech`
- ✅ Transcription: `v1/audio/transcriptions`
- ✅ Translation: `v1/audio/translations`
- ✅ Moderation: `v1/moderations`
- ✅ Completions (legacy): `v1/completions`

## Features
- **Inpainting**: Supported

## Model Snapshots
- **gpt-image-1**: Current version
- **gpt-image-1**: Alias for latest"""

def get_model_rate_limits() -> str:
    """
    Rate limits and usage tiers for GPT-Image-1 model access.
    """
    return """# GPT-Image-1 Rate Limits

## Rate Limits by Tier
| Tier | TPM | IPM |
|------|-----|-----|
| Free | Not supported | Not supported |
| Tier 1 | 100,000 | 5 |
| Tier 2 | 250,000 | 20 |
| Tier 3 | 800,000 | 50 |
| Tier 4 | 3,000,000 | 150 |
| Tier 5 | 8,000,000 | 250 |

## Legend
- **TPM**: Tokens Per Minute
- **IPM**: Images Per Minute

Rate limits ensure fair and reliable access to the API by placing specific caps on requests or tokens used within a given time period. Your usage tier determines how high these limits are set and automatically increases as you send more requests and spend more on the API."""