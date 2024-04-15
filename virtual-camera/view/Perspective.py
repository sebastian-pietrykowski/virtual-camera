class Perspective:
    INITIAL_ZOOM_FACTOR = 1.
    ZOOM_FACTOR_STEP = 1.1
    FIELD_OF_VIEW_IN_DEGREES = 60
    NEAR = 1
    FAR = 1000

    __zoom_factor = INITIAL_ZOOM_FACTOR

    def get_zoom_factor(self):
        return self.__zoom_factor

    def increase_zoom_factor(self):
        self.__zoom_factor *= Perspective.ZOOM_FACTOR_STEP

    def decrease_zoom_factor(self):
        self.__zoom_factor /= self.ZOOM_FACTOR_STEP
        if self.__zoom_factor < Perspective.INITIAL_ZOOM_FACTOR:
            self.__zoom_factor = Perspective.INITIAL_ZOOM_FACTOR
