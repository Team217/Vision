#include "WPILib.h"

class livestream: public IterativeRobot
{
private:
	IMAQdxSession session;
	Image *frame;
	IMAQdxError imaqError;

	void RobotInit()
	{
		// create an image
		frame = imaqCreateImage(IMAQ_IMAGE_RGB, 0);
		//the camera name (ex "cam0") can be found through the roborio web interface
		imaqError = IMAQdxOpenCamera("cam1", IMAQdxCameraControlModeController, &session);
		imaqError = IMAQdxConfigureGrab(session);
	}

	void AutonomousInit()
	{

	}

	void AutonomousPeriodic()
	{

	}

	void TeleopInit()
	{
		IMAQdxStartAcquisition(session);
	}

	void TeleopPeriodic()
	{
		// acquire images
		IMAQdxStartAcquisition(session);
		IMAQdxGrab(session, frame, true, NULL);
		CameraServer::GetInstance()->SetImage(frame);
	}

	void TestPeriodic()
	{

	}

};
START_ROBOT_CLASS(livestream);
