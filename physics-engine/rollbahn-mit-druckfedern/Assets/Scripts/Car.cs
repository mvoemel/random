using NUnit.Framework;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;

/**
 * Done by KPP (pern) in 2025!
 */

public class Car : MonoBehaviour
{
    // the rigid body of the car
    private Rigidbody rb;

    // the rigid body of the bumpers
    private Rigidbody leftBumper;
    private Rigidbody rightBumper;

    // the Exporter script (if attached to the game object)
    private Exporter exporter;

    // the time the car was launched
    private float launchTime;

    // flag to remember if car was launched
    private bool isLaunched = false;

    // the width of the car (could also be gotten from the collider)
    private readonly float carWidth = 0.3f;

    // the width of the bumpers (could also be gotten from the collider)
    private readonly float bumperWidth = 0.1f;

    public float impactOffset = 0.25f; 

    public enum BumperMode
    {
        BothFixed,
        LeftFree,
        LeftFreeWithFriction,
        InelasticCollision,
        InelasticCollisionWithRotation
    }

    // determines the state of the bumpers
    public BumperMode bumperMode = BumperMode.BothFixed;

    // helper flag to automatically start the car when recording starts
    // Window > General > Recorder > Start Recording
    private readonly bool recording = true;




    // initial velocity of the car
    public float initialVelocity = 0f;

    // the length of the uncompressed spring
    public float springLength = 0f;

    // spring constant
    public float springConstant = 0f;

    // friction coefficient bumper (laminare viskose D�mpfung FR=frictionCoefficient * v)
    public float frictionCoefficient = 0f;

    // Variables to track spring compressions and forces for data logging
    private float compressionLeft = 0f;
    private float forceLeft = 0f;
    private float compressionRight = 0f;
    private float forceRight = 0f;

    // Flag to use collision formulas instead of springs for right bumper
    public bool useCollisionFormulaForRightBumper = false;

    private FixedJoint fixedJoint;
    private bool collisionOccurred = false;


    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        // get the rigid body of the car
        rb = GetComponent<Rigidbody>();

        // get the rigid body of the bumpers
        leftBumper = GameObject.Find("Bumper left").GetComponent<Rigidbody>();
        rightBumper = GameObject.Find("Bumper right").GetComponent<Rigidbody>();

        // get the Exporter script
        exporter = GetComponent<Exporter>();
        Assert.IsNotNull(exporter, "Exporter script not found");

        // set motion of the bumpers
        // Your code here ...
        switch (bumperMode)
        {
            case BumperMode.BothFixed:
                ConfigureBumpersFixed();
                break;
            case BumperMode.LeftFree:
            case BumperMode.LeftFreeWithFriction:
                ConfigureBumperLeftFree();
                break;
            case BumperMode.InelasticCollision:
                ConfigureInelasticCollision();
                break;
            case BumperMode.InelasticCollisionWithRotation:
                ConfigureInelasticCollisionWithRotation();
                break;
            default:
                Assert.Fail("Invalid bumper mode");
                break;
        }


        // Note: switch off collider in the inspector, because depending on the spring paramters, it can happen that the car touches the bumpers
        // and then the movement looks very strange and debugging is difficult (try increasing initial velocity). Without collider one sees
        // that the car penetrates the bumpers and debugging becomes easier.


        // === solver settings ===

        // Controls how often physics updates occur (default: 0.02s or 50 Hz)
        Time.fixedDeltaTime = 0.02f;

        // Determines how many times Unity refines the constraint solving per physics step(default: 6)
        Physics.defaultSolverIterations = 6;

        // Similar to above but specifically for velocity constraints (default: 1)
        Physics.defaultSolverVelocityIterations = 1;
    }

    void ConfigureBumpersFixed()
    {
        // confine motion of the to 1D along z-axis
        rb.constraints = RigidbodyConstraints.FreezePositionX
                        | RigidbodyConstraints.FreezePositionY
                        | RigidbodyConstraints.FreezeRotationX
                        | RigidbodyConstraints.FreezeRotationY
                        | RigidbodyConstraints.FreezeRotationZ;

        // fix bumper in place
        leftBumper.constraints = RigidbodyConstraints.FreezeAll;
        rightBumper.constraints = RigidbodyConstraints.FreezeAll;
    }

    void ConfigureBumperLeftFree()
    {
        // confine motion of the to 1D along z-axis
        rb.constraints = RigidbodyConstraints.FreezePositionX
                        | RigidbodyConstraints.FreezePositionY
                        | RigidbodyConstraints.FreezeRotationX
                        | RigidbodyConstraints.FreezeRotationY
                        | RigidbodyConstraints.FreezeRotationZ;

        // allow bumper to move along z-axis
        // allow left bumper to move along z-axis
        leftBumper.isKinematic = false; // Make it affected by physics
        
        // constrain motion of the bumper to 1D along z-axis
        leftBumper.constraints = RigidbodyConstraints.FreezePositionX | RigidbodyConstraints.FreezePositionY | RigidbodyConstraints.FreezeRotationX | RigidbodyConstraints.FreezeRotationY | RigidbodyConstraints.FreezeRotationZ;
        
        // right bumper stays fixed
        rightBumper.constraints = RigidbodyConstraints.FreezeAll;
    }

    void ConfigureInelasticCollision()
    {
        // Expand to 2D movement as specified in Part 3
        rb.constraints = RigidbodyConstraints.FreezePositionY | 
                        RigidbodyConstraints.FreezeRotationX | 
                        RigidbodyConstraints.FreezeRotationY | 
                        RigidbodyConstraints.FreezeRotationZ;

        leftBumper.isKinematic = false;

        // Left bumper can move in 2D
        leftBumper.constraints = RigidbodyConstraints.FreezePositionY | 
                                RigidbodyConstraints.FreezeRotationX | 
                                RigidbodyConstraints.FreezeRotationY | 
                                RigidbodyConstraints.FreezeRotationZ;

        
        // Right bumper remains fixed
        rightBumper.constraints = RigidbodyConstraints.FreezeAll;
    }

    void ConfigureInelasticCollisionWithRotation()
    {
        // Allow full 2D movement and Z-axis rotation for both objects
        rb.constraints = RigidbodyConstraints.FreezePositionX |
                        RigidbodyConstraints.FreezePositionY |
                        RigidbodyConstraints.FreezeRotationX |
                        RigidbodyConstraints.FreezeRotationZ;

        leftBumper.isKinematic = false;

        leftBumper.constraints = RigidbodyConstraints.FreezePositionY;

        // Position car for off-center impact
        transform.position += new Vector3(impactOffset, 0, 0);
    }


    // Update is called once per frame
    void Update()
    {
        // launch car
        if (Keyboard.current[Key.Space].wasPressedThisFrame || (recording && !isLaunched))
        {
            LaunchCar();
        }

        // reload scene
        if (Keyboard.current[Key.R].wasPressedThisFrame)
        {
            // Reload the scene
            SceneManager.LoadScene(SceneManager.GetActiveScene().name);
        }
    }

    void LaunchCar()
    {
        // remember that car was launched
        isLaunched = true;

        // remember the current time
        launchTime = Time.time;

        // Set initial velocity of the car
        rb.linearVelocity = new Vector3(0, 0, initialVelocity);

        // log
        Debug.Log("Launching the car");
    }


    private void FixedUpdate()
    {
        if (!isLaunched) return;

         switch (bumperMode)
        {
            case BumperMode.BothFixed:
            case BumperMode.LeftFree:
            case BumperMode.LeftFreeWithFriction:
                LeftBumperSpringWithOrWithoutFriction();
                break;
            case BumperMode.InelasticCollision:
                LeftBumperInelasticCollision();
                break;
            case BumperMode.InelasticCollisionWithRotation:
                LeftBumperInelasticCollisionWithRotation();
                break;
            default:
                Assert.Fail("Invalid bumper mode");
                break;
        }

        RightBumperSpring();

        // === time series data
        // store time series record
        if (isLaunched)
        {
            ExportTimeSeriesData();
        }
    }

    void LeftBumperInelasticCollisionWithRotation()
    {
        // Detect collision and create fixed joint
        if (!collisionOccurred && IsCollisionDetected())
        {
            CreateInelasticJoint();
        }
        else if (collisionOccurred && IsCollisionDetected())
        {
            // Calculate center of mass for car and bumper system
            Vector3 carPos = rb.position;
            Vector3 bumperPos = leftBumper.position;
            float carMass = rb.mass;
            float bumperMass = leftBumper.mass;
            float totalMass = carMass + bumperMass;

            Vector3 centerOfMass = (carMass * carPos + bumperMass * bumperPos) / totalMass;

            // Calculate moment of inertia for each object (assuming rectangular prisms)
            Vector3 carScale = rb.transform.localScale;
            Vector3 bumperScale = leftBumper.transform.localScale;

            float carInertia = CalculateRectangularInertia(carMass, carScale);
            float bumperInertia = CalculateRectangularInertia(bumperMass, bumperScale);

            // Calculate distances from center of mass
            float carDistance = Vector2.Distance(
                new Vector2(carPos.x, carPos.z), 
                new Vector2(centerOfMass.x, centerOfMass.z)
            );
            float bumperDistance = Vector2.Distance(
                new Vector2(bumperPos.x, bumperPos.z), 
                new Vector2(centerOfMass.x, centerOfMass.z)
            );

            // Apply parallel axis theorem to get total moment of inertia
            float totalInertia = carInertia + carMass * Mathf.Pow(carDistance, 2) + 
                                bumperInertia + bumperMass * Mathf.Pow(bumperDistance, 2);

            // Calculate angular momentum and velocity
            Vector3 radiusVector = carPos - centerOfMass;
            Vector3 linearMomentum = carMass * rb.linearVelocity;
            float angularMomentum = Vector3.Cross(radiusVector, linearMomentum).y;

            float angularVelocity = angularMomentum / totalInertia;
            rb.angularVelocity = new Vector3(0, angularVelocity, 0);
        }
    }

    private float CalculateRectangularInertia(float mass, Vector3 scale)
    {
        return (1f / 12f) * mass * (Mathf.Pow(scale.x, 2) + Mathf.Pow(scale.z, 2));
    }

    bool IsCollisionDetected()
    {
        // Simple 1D distance-based collision detection in Z direction only
        float distanceZ = Mathf.Abs(rb.position.z - leftBumper.position.z);
        return distanceZ < 0.2f && rb.linearVelocity.z < 0; // Car moving towards bumper

        // Simple distance-based collision detection
        // float distance = Vector3.Distance(rb.position, leftBumper.position);
        // Debug.Log(distance);
        // return distance < 0.2f && rb.linearVelocity.z < 0; // Car moving towards bumper
    }

    void CreateInelasticJoint()
    {
        fixedJoint = gameObject.AddComponent<FixedJoint>();
        fixedJoint.connectedBody = leftBumper;
        // fixedJoint.breakForce = Mathf.Infinity;
        // fixedJoint.breakTorque = Mathf.Infinity;

        collisionOccurred = true;
        
        Debug.Log("Inelastic collision occurred - objects joined");
    }

    void LeftBumperInelasticCollision()
    {
        // Detect collision and create fixed joint
        if (!collisionOccurred && IsCollisionDetected())
        {
            CreateInelasticJoint();
        }
    }

    void LeftBumperSpringWithOrWithoutFriction()
    {
        float distanceToLeftBumper = Mathf.Abs(transform.position.z - leftBumper.position.z) - (carWidth / 2) - (bumperWidth / 2);

        // === left spring
        compressionLeft = 0;
        forceLeft = 0;

        if (distanceToLeftBumper < springLength)
        {
            // Calculate compression of the left spring
            compressionLeft = springLength - distanceToLeftBumper;

            // Calculate force (F = k * x)
            forceLeft = springConstant * compressionLeft;

            // Apply force to the car (away from the left bumper, in positive z direction)
            rb.AddForce(new Vector3(0, 0, forceLeft), ForceMode.Force);

            // Apply equal and opposite force to the left bumper if it's mobile
            if (bumperMode == BumperMode.LeftFree || bumperMode == BumperMode.LeftFreeWithFriction)
            {
                leftBumper.AddForce(new Vector3(0, 0, -forceLeft), ForceMode.Force);
            }
        }

        // === left bumper friction
        if (bumperMode == BumperMode.LeftFreeWithFriction)
        {
            // Apply friction to the left bumper if it's moving
            if (Mathf.Abs(leftBumper.linearVelocity.z) > 0.01f)
            {
                // Calculate friction force (F = -k * v)
                float frictionForce = -frictionCoefficient * leftBumper.linearVelocity.z;

                // Apply friction force to the left bumper
                leftBumper.AddForce(new Vector3(0, 0, frictionForce), ForceMode.Force);
            }
            else
            {
                // If velocity is very small, set it to zero to prevent endless tiny movements
                if (Mathf.Abs(leftBumper.linearVelocity.z) < 0.01f)
                {
                    leftBumper.linearVelocity = new Vector3(0, 0, 0);
                }
            }
        }
    }

    void RightBumperSpring()
    {
        float distanceToRightBumper = Mathf.Abs(transform.position.z - rightBumper.position.z) - (carWidth / 2) - (bumperWidth / 2);

        // === right spring or collision formula
        compressionRight = 0;
        forceRight = 0;

        if (!useCollisionFormulaForRightBumper)
        {
            // Use spring-based physics for right bumper
            if (distanceToRightBumper < springLength)
            {
                // Calculate compression of the right spring
                compressionRight = springLength - distanceToRightBumper;

                // Calculate force (F = k * x)
                forceRight = springConstant * compressionRight;

                // Apply force to the car (away from the right bumper, in negative z direction)
                rb.AddForce(new Vector3(0, 0, -forceRight), ForceMode.Force);
            }
        }
        else
        {
            // Use collision formulas for right bumper
            // Only apply when the car is very close to the right bumper and moving towards it
            if (distanceToRightBumper <= 0.01f && rb.linearVelocity.z > 0)
            {
                // Elastic collision: v' = -v (for fixed bumper collision)
                rb.linearVelocity = new Vector3(0, 0, -rb.linearVelocity.z);

                // Log the collision
                Debug.Log("Collision with right bumper at time: " + (Time.time - launchTime));
            }
        }
    }

    void ExportTimeSeriesData()
    {
        // Create and add data record using the provided TimeSeriesData class
        TimeSeriesData timeSeriesData = new TimeSeriesData(
            rb,
            Time.time - launchTime,
            compressionLeft,
            forceLeft,
            compressionRight,
            forceRight,
            leftBumper.position.z,
            leftBumper.linearVelocity.z
        );
        exporter.AddData(timeSeriesData);
    }

    void OnGUI()
    {
        GUIStyle textStyle = new()
        {
            fontSize = 20,
            normal = { textColor = Color.black }
        };

        // keyboard shortcuts
        GUI.Label(new Rect(10, Screen.height - 20, 400, 20),
            "R ... Reload", textStyle);
    }
}
