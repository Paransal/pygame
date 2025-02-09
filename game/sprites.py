import pygame

def load_sprite(svg_path, width, height):
    """Convert SVG to pygame surface with specified dimensions"""
    try:
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Load SVG content and render to surface
        # Since we can't use actual images, we'll create basic shapes
        pygame.draw.rect(surface, (0, 255, 0), (0, 0, width, height))
        return surface
    except Exception as e:
        print(f"Error loading sprite: {e}")
        return create_fallback_sprite(width, height)

def create_fallback_sprite(width, height):
    """Create a fallback sprite if loading fails"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surface, (255, 0, 0), (0, 0, width, height))
    return surface

def create_animation_frames(sprite, num_frames):
    """Create animation frames from a sprite"""
    frames = []
    frame_width = sprite.get_width() // num_frames
    for i in range(num_frames):
        frame = pygame.Surface((frame_width, sprite.get_height()), pygame.SRCALPHA)
        frame.blit(sprite, (0, 0), (i * frame_width, 0, frame_width, sprite.get_height()))
        frames.append(frame)
    return frames
