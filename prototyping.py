def stepper_control(directionLeftStepper, noOfStepsLeftStepper, directionRightStepper, noOfStepsRightStepper):
    pointComplete = False
    leftComplete = False
    rightComplete = False

    while pointComplete == False:

        if noOfStepsLeftStepper == 0:
            leftComplete = True

        if noOfStepsRightStepper == 0:
            rightComplete = True

        if(directionLeftStepper == "left" and leftComplete == False):
            stepperOne.step_left()
            noOfStepsLeftStepper -= 1
        if(directionLeftStepper == "right" and leftComplete == False):
            stepperOne.step_right()
            noOfStepsLeftStepper -= 1
        
        if(directionRightStepper == "left" and rightComplete == False):
            stepperTwo.step_left()
            noOfStepsRightStepper -= 1

        if(directionRightStepper == "right" and rightComplete == False):
            stepperTwo.step_right()
            noOfStepsRightStepper -= 1

        if leftComplete == True and rightComplete == True:
            pointComplete = True
