import torch
import numpy as np
from PIL import Image
import re

class AdvancedImageSelectorByPrompt:
    @classmethod
    def INPUT_TYPES(s):
        inputs = {"required": {
            "prompt": ("STRING", {"multiline": True, "default": "A photo of {@cat_image} and {@dog_image}."})
        }}
        
        optional_inputs = {}
        for i in range(15):
            char_label = chr(65 + i)
            optional_inputs[f"image_{char_label}"] = ("IMAGE",)
            optional_inputs[f"name_{char_label}"] = ("STRING", {"default": ""})
            
        inputs["optional"] = optional_inputs
        return inputs

    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "IMAGE", "IMAGE", "STRING",)
    RETURN_NAMES = ("output_1", "output_2", "output_3", "output_4", "output_5", "prompt",)
    FUNCTION = "select_images"
    CATEGORY = "Image Processing"

    def select_images(self, prompt, **kwargs):
        black_image_pil = Image.new('RGB', (64, 64), (0, 0, 0))
        black_image_np = np.array(black_image_pil).astype(np.float32) / 255.0
        black_image_tensor = torch.from_numpy(black_image_np).unsqueeze(0)

        
        name_to_image = {}
        for i in range(15):
            char_label = chr(65 + i)
            
            custom_name = kwargs.get(f"name_{char_label}", "").strip()
            
            effective_name = custom_name if custom_name else char_label
            
            image_tensor = kwargs.get(f"image_{char_label}", None)
            
            name_to_image[effective_name] = image_tensor

        
        placeholders_in_prompt = re.findall(r'\{@(.+?)\}', prompt)
        
        output_images = []
        
        for i in range(5):
            if i < len(placeholders_in_prompt):
                placeholder_name = placeholders_in_prompt[i]
                image_to_output = name_to_image.get(placeholder_name, None)
                
                if image_to_output is not None:
                    output_images.append(image_to_output)
                else:
                    output_images.append(black_image_tensor)
            else:
                output_images.append(black_image_tensor)

        
        class PromptReplacer:
            def __init__(self):
                self.count = 0
            
            def replacer_func(self, match):
                self.count += 1
                return f"参考图{self.count}"

        prompt_replacer = PromptReplacer()
        prompt_out = re.sub(r'\{@(.+?)\}', prompt_replacer.replacer_func, prompt)

        return (output_images[0], output_images[1], output_images[2], output_images[3], output_images[4], prompt_out,)

NODE_CLASS_MAPPINGS = {
    "AdvancedImageSelectorByPrompt": AdvancedImageSelectorByPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AdvancedImageSelectorByPrompt": "Adv Image Selector by Prompt -- HooToo"
}