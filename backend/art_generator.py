# # art_generator.py - Complete local implementation
# from PIL import Image, ImageDraw, ImageFilter
# import io
# import base64
# import random
# import math

# def generate_art(prompt: str) -> str:
#     try:
#         print(f"🎨 Creating local art for: {prompt}")
        
#         # Create a high-quality 512x512 image
#         width, height = 512, 512
#         image = Image.new('RGB', (width, height), color='black')
#         draw = ImageDraw.Draw(image)
        
#         # Analyze prompt for mood and style
#         mood_data = analyze_mood(prompt)
        
#         # Create layered abstract art
#         create_background(draw, width, height, mood_data)
#         create_shapes(draw, width, height, mood_data)
#         create_particles(draw, width, height, mood_data)
        
#         # Apply artistic effects
#         image = apply_effects(image, mood_data)
        
#         # Save to buffer and encode
#         buffered = io.BytesIO()
#         image.save(buffered, format="PNG", quality=95)
#         encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
#         print("✅ Local art generated successfully")
#         return encoded_image
        
#     except Exception as e:
#         print(f"❌ Local generation failed: {e}")
#         return None

# def analyze_mood(prompt):
#     """Analyze the prompt to determine artistic style and colors"""
#     prompt_lower = prompt.lower()
    
#     mood_data = {
#         'primary_colors': [],
#         'secondary_colors': [],
#         'style': 'abstract',
#         'energy_level': 5,  # 1-10
#         'complexity': 5     # 1-10
#     }
    
#     # Determine colors based on emotions
#     if any(word in prompt_lower for word in ['happy', 'joy', 'excited', 'cheerful', 'bright']):
#         mood_data['primary_colors'] = [(255, 223, 0), (255, 165, 0), (255, 215, 0)]
#         mood_data['secondary_colors'] = [(255, 255, 255), (255, 248, 220)]
#         mood_data['energy_level'] = 8
#         mood_data['style'] = 'vibrant'
        
#     elif any(word in prompt_lower for word in ['sad', 'depressed', 'blue', 'down', 'melancholy']):
#         mood_data['primary_colors'] = [(70, 130, 180), (25, 25, 112), (72, 61, 139)]
#         mood_data['secondary_colors'] = [(173, 216, 230), (176, 196, 222)]
#         mood_data['energy_level'] = 3
#         mood_data['style'] = 'flowing'
        
#     elif any(word in prompt_lower for word in ['angry', 'mad', 'furious', 'rage', 'intense']):
#         mood_data['primary_colors'] = [(220, 20, 60), (139, 0, 0), (255, 69, 0)]
#         mood_data['secondary_colors'] = [(255, 140, 0), (255, 99, 71)]
#         mood_data['energy_level'] = 9
#         mood_data['style'] = 'sharp'
        
#     elif any(word in prompt_lower for word in ['calm', 'peaceful', 'serene', 'relaxed', 'zen']):
#         mood_data['primary_colors'] = [(32, 178, 170), (95, 158, 160), (176, 224, 230)]
#         mood_data['secondary_colors'] = [(240, 248, 255), (230, 230, 250)]
#         mood_data['energy_level'] = 2
#         mood_data['style'] = 'smooth'
        
#     elif any(word in prompt_lower for word in ['love', 'romantic', 'heart', 'warm']):
#         mood_data['primary_colors'] = [(255, 20, 147), (255, 105, 180), (255, 182, 193)]
#         mood_data['secondary_colors'] = [(255, 228, 225), (255, 240, 245)]
#         mood_data['energy_level'] = 6
#         mood_data['style'] = 'soft'
        
#     elif any(word in prompt_lower for word in ['creative', 'artistic', 'inspired', 'imaginative']):
#         mood_data['primary_colors'] = [(138, 43, 226), (75, 0, 130), (148, 0, 211)]
#         mood_data['secondary_colors'] = [(221, 160, 221), (218, 112, 214)]
#         mood_data['energy_level'] = 7
#         mood_data['style'] = 'complex'
#         mood_data['complexity'] = 8
        
#     else:  # neutral/mixed emotions
#         mood_data['primary_colors'] = [(100, 149, 237), (135, 206, 235), (123, 104, 238)]
#         mood_data['secondary_colors'] = [(230, 230, 250), (248, 248, 255)]
#         mood_data['energy_level'] = 5
#         mood_data['style'] = 'balanced'
    
#     return mood_data

# def create_background(draw, width, height, mood_data):
#     """Create a gradient or textured background"""
#     colors = mood_data['primary_colors']
#     style = mood_data['style']
    
#     if style == 'flowing':
#         # Wavy gradient
#         for y in range(height):
#             wave = math.sin(y * 0.02) * 0.1 + 0.5
#             color_ratio = (y / height + wave) % 1
#             color = blend_colors(colors[0], colors[1], color_ratio)
#             draw.line([(0, y), (width, y)], fill=color)
    
#     elif style == 'sharp':
#         # Angular patterns
#         for i in range(10):
#             angle = random.random() * math.pi * 2
#             x_center = width // 2
#             y_center = height // 2
#             size = random.randint(100, 300)
            
#             points = []
#             for j in range(6):  # hexagon
#                 x = x_center + size * math.cos(angle + j * math.pi / 3)
#                 y = y_center + size * math.sin(angle + j * math.pi / 3)
#                 points.append((x, y))
            
#             color = random.choice(colors)
#             draw.polygon(points, fill=color + (100,))  # Semi-transparent
    
#     else:
#         # Smooth gradient
#         for y in range(height):
#             ratio = y / height
#             color = blend_colors(colors[0], colors[-1], ratio)
#             draw.line([(0, y), (width, y)], fill=color)

# def create_shapes(draw, width, height, mood_data):
#     """Create mood-appropriate shapes"""
#     colors = mood_data['primary_colors'] + mood_data['secondary_colors']
#     energy = mood_data['energy_level']
#     complexity = mood_data['complexity']
#     style = mood_data['style']
    
#     num_shapes = min(30, 5 + complexity * 3)
    
#     for _ in range(num_shapes):
#         color = random.choice(colors)
#         alpha = random.randint(80, 200)
        
#         if style == 'vibrant':
#             # Bright circles and stars
#             create_star_shape(draw, width, height, color, energy)
#         elif style == 'flowing':
#             # Organic, flowing shapes
#             create_organic_shape(draw, width, height, color)
#         elif style == 'sharp':
#             # Angular, geometric shapes
#             create_geometric_shape(draw, width, height, color)
#         else:
#             # Mixed shapes
#             shape_type = random.choice(['circle', 'rectangle', 'triangle'])
#             create_basic_shape(draw, width, height, color, shape_type)

# def create_star_shape(draw, width, height, color, energy):
#     """Create star-like energetic shapes"""
#     center_x = random.randint(0, width)
#     center_y = random.randint(0, height)
#     size = random.randint(20, 80)
#     points = []
    
#     for i in range(10):  # 5-pointed star
#         angle = i * math.pi / 5
#         radius = size if i % 2 == 0 else size // 2
#         x = center_x + radius * math.cos(angle)
#         y = center_y + radius * math.sin(angle)
#         points.append((x, y))
    
#     draw.polygon(points, fill=color)

# def create_organic_shape(draw, width, height, color):
#     """Create flowing, organic shapes"""
#     center_x = random.randint(0, width)
#     center_y = random.randint(0, height)
#     size = random.randint(30, 100)
    
#     # Create irregular ellipse
#     bbox = [
#         center_x - size + random.randint(-20, 20),
#         center_y - size + random.randint(-20, 20),
#         center_x + size + random.randint(-20, 20),
#         center_y + size + random.randint(-20, 20)
#     ]
#     draw.ellipse(bbox, fill=color)

# def create_geometric_shape(draw, width, height, color):
#     """Create sharp, geometric shapes"""
#     x1 = random.randint(0, width)
#     y1 = random.randint(0, height)
#     x2 = x1 + random.randint(50, 150)
#     y2 = y1 + random.randint(50, 150)
    
#     shape_type = random.choice(['rectangle', 'triangle', 'diamond'])
    
#     if shape_type == 'rectangle':
#         draw.rectangle([x1, y1, x2, y2], fill=color)
#     elif shape_type == 'triangle':
#         points = [(x1, y2), (x2, y2), ((x1+x2)//2, y1)]
#         draw.polygon(points, fill=color)
#     else:  # diamond
#         mid_x, mid_y = (x1+x2)//2, (y1+y2)//2
#         points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
#         draw.polygon(points, fill=color)

# def create_basic_shape(draw, width, height, color, shape_type):
#     """Create basic shapes"""
#     if shape_type == 'circle':
#         x = random.randint(0, width)
#         y = random.randint(0, height)
#         radius = random.randint(15, 60)
#         draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
#     elif shape_type == 'rectangle':
#         x1, y1 = random.randint(0, width), random.randint(0, height)
#         x2, y2 = x1 + random.randint(30, 100), y1 + random.randint(30, 100)
#         draw.rectangle([x1, y1, x2, y2], fill=color)

# def create_particles(draw, width, height, mood_data):
#     """Add small particle effects"""
#     energy = mood_data['energy_level']
#     colors = mood_data['secondary_colors']
    
#     num_particles = energy * 20
    
#     for _ in range(num_particles):
#         x = random.randint(0, width)
#         y = random.randint(0, height)
#         size = random.randint(1, 4)
#         color = random.choice(colors)
        
#         draw.ellipse([x, y, x+size, y+size], fill=color)

# def apply_effects(image, mood_data):
#     """Apply post-processing effects"""
#     style = mood_data['style']
    
#     if style == 'soft':
#         # Slight blur for soft emotions
#         image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
#     elif style == 'sharp':
#         # Enhance edges for intense emotions
#         image = image.filter(ImageFilter.EDGE_ENHANCE)
    
#     return image

# def blend_colors(color1, color2, ratio):
#     """Blend two RGB colors"""
#     r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
#     g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
#     b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
#     return (r, g, b)


# import requests
# import base64
# from urllib.parse import quote
# import time

# def generate_art(prompt: str) -> str:
#     try:
#         print(f"🎨 Generating art for: {prompt}")
        
#         # Enhance prompt for better artistic results based on mood
#         enhanced_prompt = enhance_prompt_for_mood(prompt)
        
#         # URL encode the prompt for the API
#         encoded_prompt = quote(enhanced_prompt)
        
#         # Generate a unique seed based on prompt to get consistent but varied results
#         seed = abs(hash(prompt + str(time.time()))) % 1000000
        
#         # Pollinations.ai - completely free, no API key needed
#         url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed={seed}&model=flux"
        
#         print(f"🌐 Requesting image from: {url[:100]}...")
        
#         # Make request with timeout
#         response = requests.get(url, timeout=45)
        
#         if response.status_code == 200:
#             # Convert image bytes to base64
#             encoded_image = base64.b64encode(response.content).decode("utf-8")
#             print("✅ Image generated successfully via Pollinations.ai")
#             return encoded_image
#         else:
#             print(f"❌ API returned status: {response.status_code}")
#             return None
            
#     except requests.exceptions.Timeout:
#         print("❌ Request timed out - try again")
#         return None
#     except Exception as e:
#         print(f"❌ Generation failed: {e}")
#         return None

# def enhance_prompt_for_mood(original_prompt):
#     """Enhance the user's prompt with artistic keywords based on detected emotions"""
    
#     prompt_lower = original_prompt.lower()
#     base_prompt = f"digital art of {original_prompt}"
    
#     # Add style based on emotional content
#     if any(word in prompt_lower for word in ['happy', 'joy', 'excited', 'cheerful']):
#         return f"{base_prompt}, bright vibrant colors, joyful, energetic, golden light, uplifting"
    
#     elif any(word in prompt_lower for word in ['sad', 'depressed', 'blue', 'down']):
#         return f"{base_prompt}, cool blue tones, melancholic, soft lighting, gentle, emotional"
    
#     elif any(word in prompt_lower for word in ['angry', 'mad', 'furious', 'rage']):
#         return f"{base_prompt}, intense red and orange colors, dramatic, powerful, dynamic"
    
#     elif any(word in prompt_lower for word in ['calm', 'peaceful', 'serene', 'relaxed']):
#         return f"{base_prompt}, peaceful, zen, soft pastels, tranquil, minimalist, harmony"
    
#     elif any(word in prompt_lower for word in ['love', 'romantic', 'heart']):
#         return f"{base_prompt}, warm pink and purple tones, romantic, soft, dreamy, beautiful"
    
#     elif any(word in prompt_lower for word in ['creative', 'artistic', 'inspired']):
#         return f"{base_prompt}, abstract, creative, colorful, artistic masterpiece, imaginative"
    
#     else:
#         return f"{base_prompt}, beautiful, artistic, high quality, detailed, colorful"

import requests
import base64
from urllib.parse import quote
import time

def generate_art(prompt: str, style: str = "realistic") -> str:
    try:
        print(f"🎨 Generating {style} art for: {prompt}")
        
        # Enhance prompt based on selected style and mood
        enhanced_prompt = enhance_prompt_with_style(prompt, style)
        
        # URL encode the prompt for the API
        encoded_prompt = quote(enhanced_prompt)
        
        # Generate a unique seed based on prompt and style
        seed = abs(hash(prompt + style + str(time.time()))) % 1000000
        
        # Pollinations.ai with style-specific model selection
        model = get_model_for_style(style)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed={seed}&model={model}"
        
        print(f"🌐 Requesting {style} image from API...")
        
        # Make request with timeout
        response = requests.get(url, timeout=45)
        
        if response.status_code == 200:
            # Convert image bytes to base64
            encoded_image = base64.b64encode(response.content).decode("utf-8")
            print(f"✅ {style.capitalize()} art generated successfully!")
            return encoded_image
        else:
            print(f"❌ API returned status: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - try again")
        return None
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return None

def get_model_for_style(style):
    """Select the best model for each art style"""
    style_models = {
        "realistic": "flux",
        "anime": "flux",
        "abstract": "flux", 
        "oil_painting": "flux",
        "cyberpunk": "flux",
        "watercolor": "flux",
        "sketch": "flux",
        "vintage": "flux"
    }
    return style_models.get(style, "flux")

def enhance_prompt_with_style(original_prompt, style):
    """Enhance the user's prompt with style-specific keywords"""
    
    prompt_lower = original_prompt.lower()
    
    # Base emotion enhancement
    emotion_enhancement = get_emotion_enhancement(prompt_lower)
    
    # Style-specific enhancements
    style_enhancements = {
        "realistic": "photorealistic, highly detailed, professional photography, cinematic lighting, 8k resolution",
        
        "anime": "anime style, manga art, Studio Ghibli inspired, cel shading, vibrant colors, Japanese animation",
        
        "abstract": "abstract art, geometric shapes, modern art, minimalist, bold colors, contemporary design",
        
        "oil_painting": "oil painting, classical art, renaissance style, brushstrokes visible, rich textures, artistic masterpiece",
        
        "cyberpunk": "cyberpunk, neon lights, futuristic, digital art, sci-fi, urban landscape, high tech low life",
        
        "watercolor": "watercolor painting, soft edges, flowing colors, artistic, traditional painting, delicate brushwork",
        
        "sketch": "pencil sketch, hand drawn, artistic sketch, black and white, detailed line art, traditional drawing",
        
        "vintage": "vintage style, retro, old-fashioned, sepia tones, nostalgic, classic photography, aged look"
    }
    
    style_prompt = style_enhancements.get(style, "artistic, beautiful, high quality")
    
    # Combine everything
    enhanced_prompt = f"{style_prompt}, {emotion_enhancement}, {original_prompt}, masterpiece, highly detailed"
    
    return enhanced_prompt

def get_emotion_enhancement(prompt_lower):
    """Get emotion-specific enhancements"""
    
    if any(word in prompt_lower for word in ['happy', 'joy', 'excited', 'cheerful']):
        return "bright vibrant colors, joyful atmosphere, energetic, golden light, uplifting mood"
    
    elif any(word in prompt_lower for word in ['sad', 'depressed', 'blue', 'down']):
        return "cool blue tones, melancholic atmosphere, soft lighting, gentle, emotional depth"
    
    elif any(word in prompt_lower for word in ['angry', 'mad', 'furious', 'rage']):
        return "intense red and orange colors, dramatic lighting, powerful, dynamic composition"
    
    elif any(word in prompt_lower for word in ['calm', 'peaceful', 'serene', 'relaxed']):
        return "peaceful atmosphere, zen, soft pastels, tranquil mood, minimalist, harmony"
    
    elif any(word in prompt_lower for word in ['love', 'romantic', 'heart']):
        return "warm pink and purple tones, romantic atmosphere, soft lighting, dreamy, beautiful"
    
    elif any(word in prompt_lower for word in ['creative', 'artistic', 'inspired']):
        return "abstract elements, creative composition, colorful, artistic masterpiece, imaginative"
    
    elif any(word in prompt_lower for word in ['fear', 'scared', 'anxiety']):
        return "dark tones, mysterious atmosphere, dramatic shadows, intense mood"
    
    else:
        return "beautiful colors, artistic composition, balanced mood"

# Function to get available styles for the frontend
def get_available_styles():
    """Return list of available art styles"""
    return {
        "realistic": {
            "name": "Realistic",
            "description": "Photorealistic, detailed artwork",
            "icon": "📷"
        },
        "anime": {
            "name": "Anime", 
            "description": "Japanese animation style",
            "icon": "🎌"
        },
        "abstract": {
            "name": "Abstract",
            "description": "Modern abstract art",
            "icon": "🎨"
        },
        "oil_painting": {
            "name": "Oil Painting",
            "description": "Classical painting style",
            "icon": "🖼️"
        },
        "cyberpunk": {
            "name": "Cyberpunk",
            "description": "Futuristic neon style",
            "icon": "🌆"
        },
        "watercolor": {
            "name": "Watercolor",
            "description": "Soft watercolor painting",
            "icon": "🎭"
        },
        "sketch": {
            "name": "Sketch",
            "description": "Hand-drawn pencil art",
            "icon": "✏️"
        },
        "vintage": {
            "name": "Vintage",
            "description": "Retro nostalgic style",
            "icon": "📼"
        }
    }