

## Calibration


#### frame 1
Firstly, let me briefly explain what is extrinsic calibration. The extrinsic calibration is the process of estimating
the transformation relation between sensors, in our project, aims to camera and radar. As shown in this figure, radar sensor 
and vision sensor are in different locations.  Targets information, such as this pedestrian are collected for both sensors.
With the extrinsic calibration, we can confirm one object in different sensors. This is the fundamental to information fusion.

#### frame 2
But how to calculate the transformation relation between sensors?  We will explain it in mathematical view. The transformation
matrix for extrinsic calibration can be expressed like this. R represents three multiple three rotation matrix and t represents as
3 multiple one translation vector. Based on this matrix, information from different sensors will be processed in the one same coordinate.

#### frame 3
Moreover, there are multiple strategies to estimate this calibration matrix. I will specific one way which is ued in our project. The mathematical equation is shown. 
In this strategy, we need to obtained k different locations of the camera and radar points. In this equation, the first P represent the set of radar points, the second represents the
set of radar point. T represent the calibrate transformation matrix. The epsilon represents the transformation error. Based on this equation, sensor calibration problem is transferred to
minimizing the transformation error. We use sequential least squares programming from scipy library to optimize this equation.

#### frame 4
Not only an efficient minimizing strategy, it is also essential that getting precise target locations for both vision and radar sensor.
Thus, a well-designed target is required. Our self-designed calibration target is shown, radar and camera can accurately obtain the positions of this target simultaneously.
Our self-designed calibration target is consist of a trihedral corner reflector and a acrylic board with a checkboard on it.  For the camera, the location features of the black and white checkerboard can be detected precisely and efficiently. For radar, the triangular corner retroreflector is the most common choice, which has distinguished localization and detection properties for radar. Expressly, radar can reflect a trihedral corner reflector with a specific RCS range and localization information.  Moreover,  the acrylic board  do not affect radar detection.


### frame 5
Although our proposed calibration approach should be available in theory, it is hard to test in real environment. Because the radar points are noisy and unreliable. What's more, the real world calibration daata
lack ground truth. So we can not directly do quantitative analysis in real world. 

### frame 6
Instead, we firstly design some calibration data ased on different number of locations and noise levels.  According to different noise novel data
, we can estimate the robustness of our calibration approach. Based on different number of locations, we can estimate the efficiency of our approach.


### frame 7
Based on our designed simulation datasets, we process the following annlysis, showning in figures. The left one shows the plot of RMSE calibration error and gaussian noise level.
As we can see, the RMSE of calibration increase linearly with noise level ofr both translation vector and rotation matrix. We can conclude that our calibration approach is robustness,
even if the noise in a high level, the error still in a stable level. On the other hand, the right figure show the RMSE for various number of location of the calibration target.
It can be seen that the calibration error declines and fluctuates to a stable low level when the target locations increase to more than 10. We indicate that with our calibration
approach, only 10 different locations of calibration target can estimate a precise calibration result. 


### frame 8
After to successful simulation test, we can implement our algorithms in real world. Left one is the calibration scenes of this outdoor experiment. To reduce environmental noise, we choose to implement the
calibration method in an empty square. Right one is the result of this experiment, displaying the detected calibration target locations for all three sensors in the camera reference frame. We can see that
camera points and radar points are well-paired, showing the good convergence of our calibration approach. 


## Algorithms




