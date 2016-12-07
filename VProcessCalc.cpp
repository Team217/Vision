#include "WPILib.h"
#include <unistd.h>
#include <stdio.h>

class Robot: public IterativeRobot
{
	private:

	//locations of vision files in roborio's file system
	const char *JAVA = "/usr/local/frc/JRE/bin/java";
	char *GRIP_ARGS[5] = { "java", "-jar", "/home/lvuser/grip.jar", "/home/lvuser/project.grip", NULL };

	SendableChooser *chooser;
	std::shared_ptr<NetworkTable> table;

	//variables and vectors to hold vision values
	float objxCur = 0;//what will change
	float const objxI = 0.002;//lower this bc jerking
	float const objxP = 0.007;//lower this bc jerking
	float const objxTar = 160;//1/2 * image width
	std::vector<double> centerYV, centerXV, areaV;
	float objxCur1=0;

	//Declare Stuff
	CANTalon *left, *right;
	Joystick *driver;

	//drivebase variables
	float lThrottle = 0;
	float rThrottle = 0;
	float cumcogPIDError = 0;
	void RobotInit()
	{
		chooser = new SendableChooser();

		//connect to network table under table GRIP
		table = NetworkTable::GetTable("GRIP");

		//initialize stuff
		left = new CANTalon(3);//left
		right = new CANTalon(5);//right
		driver = new Joystick(0);

		//create a separate process that runs the .grip file
		if (fork() == 0)
		{
			if (execv(JAVA, GRIP_ARGS) == -1)
			{
				perror("Error running GRIP");//if it fails to start throws error
			}
		}
	}

	void AutonomousInit()
	{

	}

	void AutonomousPeriodic()
	{

	}

	void TeleopInit()
	{

	}

	void TeleopPeriodic()
	{

	}

	void TestPeriodic()
	{
		networkTableGrab();
		printVision();
		if (driver->GetRawButton(1) && areaV[0] > 3000)
		{

			left->Set(-visionPID(objxTar, objxCur, objxP, objxI) * .5);
			right->Set(-visionPID(objxTar, objxCur, objxP, objxI) * .5);
		}
		else
		{
			tankDrive();
		}

	}

	void TestInit()
	{
		cumcogPIDError = 0;
	}
	//standard PID that has both P and I implemented (Target, currentPosition,P constant,I constant
	float visionPID(float cogTar, float cogpos, float cogP, float cogI)
	{
		float cogPIDTar = cogTar;
		float cogPIDPos = cogpos;
		float cogPIDError = cogPIDTar - cogPIDPos;
		cumcogPIDError = cogPIDError + cumcogPIDError;
		float cogPIDPout = cogPIDError * cogP;
		float cogPIDIout = cumcogPIDError * cogI;
		float cogPIDSpeed = cogPIDPout + cogPIDIout;
		return cogPIDSpeed;
	}

	void networkTableGrab()
	{
		//retrieve arrays from network tables
		centerYV = table->GetNumberArray("myContoursReport/centerY", llvm::ArrayRef<double>());
		centerXV = table->GetNumberArray("myContoursReport/centerX", llvm::ArrayRef<double>());
		areaV = table->GetNumberArray("myContoursReport/area", llvm::ArrayRef<double>());
	}
	//print everything in arrays
	void printVision()
	{
		for (auto centerY : centerYV)
		{
			std::cout << "centerY: " << centerY << std::endl;
		}
		for (auto centerX : centerXV)
		{
			std::cout << "centerX: " << centerX << std::endl;
		}
		for (auto area : areaV)
		{
			std::cout << "area: " << area << std::endl;
		}

		//TODO: determine which vextor index get is corect

		objxCur = centerXV[0];
		objxCur1 = centerXV[1];
		std::cout << "objxCur[]: " << objxCur << std::endl;
		std::cout << "objxCur1[]: " << objxCur1 << std::endl;

		objxCur = centerXV.at(0);
		objxCur1 = centerXV.at(1);
		std::cout << "objxCurAT: " << objxCur << std::endl;
		std::cout << "objxCur1AT: " << objxCur1 << std::endl;
	}

	void tankDrive()
	{
		lThrottle = Deadband(driver->GetY());
		rThrottle = -Deadband(driver->GetRawAxis(5));//Throttle or Twist based on controller used
		left->Set(lThrottle);
		right->Set(rThrottle);

	}
	float Deadband(float input)
	{
		if (input > .05 || input < -.05)
		{
			return input;

		}
		else
		{
			return 0;
		}
		return input;
	}
};

START_ROBOT_CLASS(Robot)
