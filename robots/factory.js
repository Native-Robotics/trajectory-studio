/**
 * factory.js
 * Factory to retrieve the correct robot configuration instance by model name.
 */
import { BaseRobot } from './base.js';
import { DobotCR30h } from './dobot.js';
import { AuboIS20 } from './aubo.js';
import { AuboIS25 } from './aubo_is25.js?v=2';
import { DobotCR20A } from './dobot_cr20a.js';
import { DoosanRobot } from './doosan.js';
import { UniversalRobot } from './ur.js';

export function getRobotConfig(modelName) {
  const name = (modelName || '').toLowerCase();
  if (name.includes('cr20a') || name.includes('cr20')) {
    return new DobotCR20A();
  } else if (name.includes('dobot')) {
    return new DobotCR30h();
  } else if (name.includes('aubo-is25') || name.includes('is25')) {
    return new AuboIS25();
  } else if (name.includes('aubo-is20') || name.includes('is20') || name.includes('aubo')) {
    return new AuboIS20();
  } else if (name.includes('doosan') || name.includes('h2017') || name.includes('p3020')) {
    return new DoosanRobot(name);
  } else if (name.includes('universal') || name.includes('ur-') || name.includes('ur10') || name.includes('ur20')) {
    return new UniversalRobot(name);
  }
  return new BaseRobot(); // Fallback
}
