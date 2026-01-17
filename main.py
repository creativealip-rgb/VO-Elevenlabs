"""
ElevenLabs Text-to-Speech Generator
Dengan fitur auto-rotate API keys
"""

from voice_gen.api_utils.eleven_api import ElevenLabsLimitException
from voice_gen.audio.eleven_voice_module import ElevenLabsVoiceModule


# Load all API keys from file
def load_api_keys():
    with open("api_keys.txt", "r") as f:
        keys = [line.strip() for line in f.readlines() if line.strip()]
    return keys


# Save current key index
def save_current_index(index):
    with open("current_key_index.txt", "w") as f:
        f.write(str(index))


# Load current key index
def load_current_index():
    try:
        with open("current_key_index.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0


def generate_voice(text, output_file="output/output.mp3", voice_id="c470sxKWDq6tA74TL3yB", min_credits=100):
    """
    Generate voice with auto-rotation of API keys when credits run low.
    
    Args:
        text: Text to convert to speech
        output_file: Output MP3 filename
        voice_id: ElevenLabs voice ID (default: Kennisa)
        min_credits: Minimum credits required, will rotate if below this
    """
    api_keys = load_api_keys()
    current_index = load_current_index()
    
    print(f"🎙️ Generating voice...")
    print(f"📋 Total API keys available: {len(api_keys)}")
    print(f"🔑 Starting with key #{current_index + 1}")
    
    attempts = 0
    max_attempts = len(api_keys)
    
    while attempts < max_attempts:
        current_key = api_keys[current_index]
        print(f"\n--- Using API Key #{current_index + 1} ---")
        
        try:
            voice_module = ElevenLabsVoiceModule(
                api_key=current_key, 
                voiceName=voice_id, 
                checkElevenCredits=True
            )
            
            remaining = voice_module.get_remaining_characters()
            print(f"💰 Available credits: {remaining}")
            
            # Check if enough credits
            if remaining < min_credits:
                print(f"⚠️ Credits too low ({remaining} < {min_credits}), rotating to next key...")
                current_index = (current_index + 1) % len(api_keys)
                save_current_index(current_index)
                attempts += 1
                continue
            
            # Generate voice
            voice_module.generate_voice(text, output_file)
            print(f"✅ Voice generated successfully!")
            print(f"📁 Saved to: {output_file}")
            print(f"💰 Remaining credits: {voice_module.get_remaining_characters()}")
            
            # Save current index for next run
            save_current_index(current_index)
            return True
            
        except ElevenLabsLimitException as e:
            print(f"❌ API Key #{current_index + 1} limit reached: {e}")
            current_index = (current_index + 1) % len(api_keys)
            save_current_index(current_index)
            attempts += 1
            
        except Exception as e:
            print(f"❌ Error with API Key #{current_index + 1}: {e}")
            current_index = (current_index + 1) % len(api_keys)
            save_current_index(current_index)
            attempts += 1
    
    print(f"\n❌ All {len(api_keys)} API keys exhausted! Please add more keys to api_keys.txt")
    return False


def check_all_credits():
    """Check remaining credits for all API keys"""
    api_keys = load_api_keys()
    print(f"\n{'='*50}")
    print(f"📊 Checking credits for all {len(api_keys)} API keys...")
    print(f"{'='*50}\n")
    
    total_credits = 0
    for i, key in enumerate(api_keys):
        try:
            voice_module = ElevenLabsVoiceModule(
                api_key=key, 
                voiceName="c470sxKWDq6tA74TL3yB", 
                checkElevenCredits=False
            )
            credits = voice_module.get_remaining_characters()
            total_credits += credits
            status = "✅" if credits >= 100 else "⚠️"
            print(f"{status} Key #{i+1}: {credits:,} characters")
        except Exception as e:
            print(f"❌ Key #{i+1}: Error - {e}")
    
    print(f"\n{'='*50}")
    print(f"💰 Total available credits: {total_credits:,} characters")
    print(f"{'='*50}")
    return total_credits


if __name__ == '__main__':
    check_all_credits()
