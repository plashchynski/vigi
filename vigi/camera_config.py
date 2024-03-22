class CameraConfig:
    def __init__(self):
        self.camera_id = 0
        self.max_errors = 50
        self.sensitivity = 0.5

    def set_camera_id(self, camera_id):
        # validate the camera id
        camera_id = int(camera_id)
        if camera_id < 0:
            raise ValueError('Camera id must be a positive integer')
        self.camera_id = camera_id

    def set_max_errors(self, max_errors):
        # set the maximum number of consecutive errors when reading a frame from the camera
        max_errors = int(max_errors)
        if max_errors < 0:
            raise ValueError('Max errors must be a positive integer')
        self.max_errors = max_errors

    def set_sensitivity(self, sensitivity):
        # set the sensitivity of the motion detector
        sensitivity = float(sensitivity)
        if sensitivity < 0 or sensitivity > 1:
            raise ValueError('Sensitivity must be between 0 and 1')
        self.sensitivity = sensitivity
