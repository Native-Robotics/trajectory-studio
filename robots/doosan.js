/**
 * doosan.js
 * Visual configuration class for Doosan robots (H2017, P3020, etc.).
 */
import { BaseRobot } from './base.js';

export class DoosanRobot extends BaseRobot {
  constructor(modelName = "doosan-h2017") {
    super();
    this.modelName = modelName;
    this.pedestalRadius = 0.15;
    this.columnRadius = 0.13;
    // Doosan robots have wider base and shoulder joints
    this.jointRingRadii = [0.135, 0.135, 0.10, 0.10, 0.08, 0.08];
    this.jointRingHeights = [0.13, 0.13, 0.10, 0.10, 0.08, 0.08];
  }
}
