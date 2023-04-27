class PeakStatistics:
    def __init__(self, wavelength: float, intensity: float, intensity_normalized: float, score: float, index: int, above_noise: bool):
        self.__wavelength: float = wavelength
        self.__intensity: float = intensity
        self.__intensity_normalized: float = intensity_normalized
        self.__score: float = score
        self.__index: int = index
        self.__above_noise: bool = above_noise

    def wavelength(self) -> float:
        return self.__wavelength

    def intensity(self) -> float:
        return self.__intensity

    def intensity_normalized(self) -> float:
        return self.__intensity_normalized

    def score(self) -> float:
        return self.__score

    def index(self) -> float:
        return self.__index

    def is_above_noise(self) -> bool:
        return self.__above_noise
