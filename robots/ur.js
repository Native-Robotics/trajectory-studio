/**
 * ur.js
 * Visual configuration class for Universal Robots (UR10, UR20, etc.).
 */
import { BaseRobot } from './base.js';

export class UniversalRobot extends BaseRobot {
  constructor(modelName = "universal_robots-ur-20") {
    super();
    this.modelName = modelName;
    this.pedestalRadius = 0.13;
    this.columnRadius = 0.11;
    this.jointRingRadii = [0.11, 0.11, 0.085, 0.085, 0.065, 0.065];
    this.jointRingHeights = [0.11, 0.11, 0.09, 0.09, 0.075, 0.075];
  }
}
