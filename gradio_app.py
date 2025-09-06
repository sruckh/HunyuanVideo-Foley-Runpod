#!/usr/bin/env python3
"""
HunyuanVideo-Foley Gradio Application for RunPod
"""

import os
import sys
import gradio as gr
import torch
from typing import Optional, Tuple
from pathlib import Path
import subprocess
import time

# Global variables for model paths
HIFIFILEY_MODEL_PATH = os.environ.get('HIFIFILEY_MODEL_PATH', '/app/HunyuanVideo-Foley/HunyuanVideo-Foley')
HUNYUAN_FOLEY_PATH = '/app/HunyuanVideo-Foley'

def check_prerequisites():
    """Check if all required components are available"""
    print("🔍 Checking prerequisites...")
    
    # Check if CUDA is available
    if not torch.cuda.is_available():
        print("⚠️  CUDA not available, using CPU mode")
    else:
        print(f"✅ CUDA available: {torch.cuda.get_device_name()}")
    
    # Check if model directory exists
    model_path = Path(HIFIFILEY_MODEL_PATH)
    if not model_path.exists():
        print(f"❌ Model path does not exist: {HIFIFILEY_MODEL_PATH}")
        raise FileNotFoundError(f"Model path {HIFIFILEY_MODEL_PATH} not found")
    
    print("✅ All prerequisites met")

def generate_video_with_foley(
    prompt: str,
    negative_prompt: str = "",
    video_length: int = 8,
    resolution: str = "512",
    seed: int = -1,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5
) -> Tuple[str, str]:
    """
    Generate video with Foley audio
    
    Returns:
        Tuple of (video_path, audio_path)
    """
    try:
        print(f"🎬 Generating video for prompt: {prompt}")
        
        # Change to HunyuanVideo-Foley directory
        original_cwd = os.getcwd()
        os.chdir(HUNYUAN_FOLEY_PATH)
        
        # Generate unique output name
        timestamp = int(time.time())
        output_name = f"output_{timestamp}"
        video_output = f"{output_name}.mp4"
        audio_output = f"{output_name}_foley.wav"
        
        # Build command for HunyuanVideo-Foley
        cmd = [
            "python3", "gradio_app.py",
            "--prompt", prompt,
            "--negative_prompt", negative_prompt,
            "--video_length", str(video_length),
            "--resolution", resolution,
            "--num_inference_steps", str(num_inference_steps),
            "--guidance_scale", str(guidance_scale),
            "--model_path", HIFIFILEY_MODEL_PATH,
            "--output_video", video_output,
            "--output_audio", audio_output
        ]
        
        if seed >= 0:
            cmd.extend(["--seed", str(seed)])
        
        print(f"🚀 Running command: {' '.join(cmd)}")
        
        # Run the generation
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            error_msg = f"Video generation failed: {result.stderr}"
            print(f"❌ {error_msg}")
            return None, None, error_msg
        
        # Check if files were created
        video_path = video_output if os.path.exists(video_output) else None
        audio_path = audio_output if os.path.exists(audio_output) else None
        
        print(f"✅ Generation complete: Video={video_path}, Audio={audio_path}")
        
        os.chdir(original_cwd)
        return video_path, audio_path, "Generation successful!"
        
    except Exception as e:
        os.chdir(original_cwd)
        error_msg = f"Error during generation: {str(e)}"
        print(f"❌ {error_msg}")
        return None, None, error_msg

def create_gradio_interface():
    """Create the Gradio interface"""
    
    interface = gr.Interface(
        fn=generate_video_with_foley,
        inputs=[
            gr.Textbox(
                label="Prompt",
                placeholder="A realistic video of...",
                lines=3,
                max_lines=5
            ),
            gr.Textbox(
                label="Negative Prompt (optional)",
                placeholder="blurry, distorted, low quality",
                lines=2,
                max_lines=3
            ),
            gr.Slider(
                minimum=4,
                maximum=16,
                step=1,
                value=8,
                label="Video Length (seconds)"
            ),
            gr.Dropdown(
                choices=["256", "512", "768", "1024"],
                value="512",
                label="Resolution"
            ),
            gr.Number(
                label="Seed (-1 for random)",
                value=-1
            ),
            gr.Slider(
                minimum=20,
                maximum=100,
                step=1,
                value=50,
                label="Inference Steps"
            ),
            gr.Slider(
                minimum=1.0,
                maximum=20.0,
                step=0.5,
                value=7.5,
                label="Guidance Scale"
            )
        ],
        outputs=[
            gr.Video(label="Generated Video"),
            gr.Audio(label="Foley Audio"),
            gr.Text(label="Status")
        ],
        title="HunyuanVideo-Foley Generator",
        description="AI-powered video generation with synchronized Foley sound effects. Based on HunyuanVideo-Foley by Tencent.",
        examples=[
            ["A astronaut walking on Mars surface", "blurry, distorted", 8, "512", -1, 50, 7.5],
            ["A beautiful sunset over ocean waves", "dark, unclear", 8, "512", -1, 50, 7.5]
        ],
        theme="default",
        allow_flagging="never"
    )
    
    return interface

def main():
    """Main function to start the application"""
    
    print("🎯 Starting HunyuanVideo-Foley Gradio Application...")
    
    try:
        # Check if HunyuanVideo-Foley exists
        if not os.path.exists(HUNYUAN_FOLEY_PATH):
            print(f"❌ HunyuanVideo-Foley not found at {HUNYUAN_FOLEY_PATH}")
            print("📋 Please ensure the repository is cloned during runtime installation")
            sys.exit(1)
        
        # Check prerequisites
        check_prerequisites()
        
        # Create and launch Gradio interface
        interface = create_gradio_interface()
        
        print("🚀 Launching Gradio server...")
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=True,
            debug=True,
            show_error=True,
            auth=None
        )
        
    except Exception as e:
        print(f"❌ Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()