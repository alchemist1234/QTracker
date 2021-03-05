import numpy as np

from item import FrameItem, ParticleGroup, SceneConfig
from typing import Dict, Any


class FrameData(object):
    def __init__(self, frame_index: int, frame: np.ndarray, particles: Dict[int, Any]):
        self.frame_index = frame_index
        self.frame = frame
        self.particles = particles

    def get_frame_item(self, config: SceneConfig):
        if self.frame is not None:
            return FrameItem(self.frame_index, self.frame)
        return None

    def get_particle_items(self, config: SceneConfig) -> Dict[int, ParticleGroup]:
        items = {}
        for index, pos in self.particles.items():
            x, y = pos
            particle_group = ParticleGroup(self.frame_index, index, x, y, config)
            items[index] = particle_group
        return items
