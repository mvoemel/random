# Physics Engine - Report Part 2

## Task 1: Compression Springs

Two compression springs are connected to the left and right bumpers. The rest length of each spring is 15 cm, and the spring constant is 10 N/m.

For each spring, the code:

1. Calculates the distance between the car and the bumper
2. Determines if the spring is compressed (distance < rest length)
3. Calculates the compression amount and resulting force using Hooke's law (F = k \* x)
4. Applies the force to the car and, if applicable, to the left bumper

```csharp
// Calculate compression of the spring
compressionLeft = springLength - distanceToLeftBumper;
// Calculate force (F = k * x)
forceLeft = springConstant * compressionLeft;
// Apply force to the car
rb.AddForce(new Vector3(0, 0, forceLeft), ForceMode.Force);
```

This causes the car to oscillate between the bumpers, with the springs pushing it away when compressed.

## Task 2: Collision Formulas

The `useCollisionFormulaForRightBumper` boolean flag is used to determine whether to use the spring-based approach or direct collision formulas for the right bumper.
When set to `true`, the code uses the following collision formula:

```csharp
// Elastic collision: v' = -v (for fixed bumper collision)
rb.velocity = new Vector3(0, 0, -rb.velocity.z);
```

This directly reverses the car's velocity when it hits the right bumper, simulating a perfectly elastic collision with a fixed barrier.

## Task 3: Free-Moving Left Bumper without Friction

For `bumperMode = 1`, the left bumper can move freely without friction. The implementation:

1. Makes the left bumper non-kinematic so it's affected by physics
2. Constrains its motion to the z-axis only
3. Applies the same spring force to both the car and the bumper, but in opposite directions

This creates an elastic collision between the car and the left bumper, where momentum is exchanged according to physics laws.

## Task 4: Left Bumper with Friction

For `bumperMode = 2`, the left bumper moves with damping friction:

```csharp
// Calculate friction force (F = -k * v)
float frictionForce = -frictionCoefficient * leftBumper.velocity.z;
// Apply friction force to the left bumper
leftBumper.AddForce(new Vector3(0, 0, frictionForce), ForceMode.Force);
```

The friction is proportional to the bumper's velocity (F = k \* v), which will cause the bumper to slow down over time. The `frictionCoefficient` value can be adjusted to achieve the desired behavior, where the bumper moves 2-3 times before the system comes to rest.
