/**
 * charts.js
 * Joint graphs management using Chart.js.
 */

import { getJointCount } from './robot.js?v=37';
import { buildMetricSeries, detectAccelerationSteps, groupStepsByTime } from './series.js?v=1';

// Custom plugin to draw a vertical timeline cursor line
const verticalCursorPlugin = {
  id: 'verticalCursor',
  afterDraw: (chart) => {
    const cursorOpts = chart.options.plugins.verticalCursor;
    if (cursorOpts && cursorOpts.timeVal !== null) {
      const timeVal = cursorOpts.timeVal;
      const ctx = chart.ctx;
      const xAxis = chart.scales.x;
      const yAxis = chart.scales.y;
      
      if (timeVal >= xAxis.min && timeVal <= xAxis.max) {
        const xPixel = xAxis.getPixelForValue(timeVal);
        
        ctx.save();
        ctx.beginPath();
        ctx.strokeStyle = '#22d3ee'; // Bright Cyan cursor
        ctx.lineWidth = 1.5;
        ctx.setLineDash([4, 4]); // Dashed line
        
        // Draw line
        ctx.moveTo(xPixel, yAxis.top);
        ctx.lineTo(xPixel, yAxis.bottom);
        ctx.stroke();
        
        // Draw small handle circle at top
        ctx.beginPath();
        ctx.arc(xPixel, yAxis.top, 4, 0, 2 * Math.PI);
        ctx.fillStyle = '#22d3ee';
        ctx.fill();
        
        ctx.restore();
      }
    }
  }
};

// Custom plugin to align the play slider with the chart's vertical grid edges
const alignSliderPlugin = {
  id: 'alignSlider',
  afterLayout: (chart) => {
    if (!chart.chartArea) return;
    const left = chart.chartArea.left;
    const right = chart.width - chart.chartArea.right;
    const bottom = chart.chartArea.bottom;
    
    const sliderWrapper = document.getElementById('timeline-slider-wrapper');
    if (sliderWrapper) {
      sliderWrapper.style.left = `${left}px`;
      sliderWrapper.style.right = `${right}px`;
      sliderWrapper.style.top = `${bottom - 9}px`; // Center directly on bottom x-axis line
    }

    const controlsRow = document.getElementById('timeline-controls-row');
    if (controlsRow) {
      controlsRow.style.left = `${left}px`;
      controlsRow.style.right = `${right}px`;
    }
  }
};

// Custom plugin to draw horizontal joint limit lines when approached within 5%
const horizontalLimitsPlugin = {
  id: 'horizontalLimits',
  afterDraw: (chart) => {
    const limits = chart.options.plugins.horizontalLimits;
    if (limits && limits.lines && limits.lines.length > 0) {
      const ctx = chart.ctx;
      const xAxis = chart.scales.x;
      const yAxis = chart.scales.y;
      
      ctx.save();
      
      limits.lines.forEach(line => {
        const yPixel = yAxis.getPixelForValue(line.value);
        if (yPixel >= yAxis.top && yPixel <= yAxis.bottom) {
          ctx.beginPath();
          ctx.strokeStyle = line.color || '#ef4444';
          ctx.lineWidth = line.width || 1.0;
          ctx.setLineDash(line.dash || [4, 4]); // Custom dash or solid
          ctx.moveTo(xAxis.left, yPixel);
          ctx.lineTo(xAxis.right, yPixel);
          ctx.stroke();
          
          // Draw text label near the line (left-aligned above the line)
          ctx.fillStyle = line.color || '#ef4444';
          ctx.font = '9px "JetBrains Mono", monospace';
          ctx.fillText(line.label, xAxis.left + 8, yPixel - 4);
        }
      });
      ctx.restore();
    }
  }
};

const STEP_KIND_LABELS = { start: 'start from rest', end: 'stop at rest', junction: 'part junction', knot: 'knot' };

// Custom plugin to mark acceleration steps (jerk impulses) on the acceleration and jerk charts
const accelerationStepsPlugin = {
  id: 'accelerationSteps',
  afterDatasetsDraw: (chart) => {
    const opts = chart.options.plugins.accelerationSteps;
    if (!opts || !opts.groups || opts.groups.length === 0) return;
    if (opts.metric !== 'acceleration' && opts.metric !== 'jerk') return;
    const ctx = chart.ctx;
    const xAxis = chart.scales.x;
    const yAxis = chart.scales.y;
    const area = chart.chartArea;
    const colors = opts.colors || [];
    const colorOf = (joint) => colors[joint % colors.length] || '#e2e8f0';
    const clampY = (y) => Math.max(area.top, Math.min(area.bottom, y));
    const maxStep = Math.max(...opts.groups.flatMap(g => g.steps.map(s => Math.abs(s.step))));

    ctx.save();
    const labelBoxes = [];
    opts.groups.forEach(group => {
      if (group.t < xAxis.min || group.t > xAxis.max) return;
      const x = xAxis.getPixelForValue(group.t);

      // Faint vertical guide at the step time
      ctx.beginPath();
      ctx.strokeStyle = 'rgba(248, 250, 252, 0.18)';
      ctx.lineWidth = 1;
      ctx.setLineDash([2, 3]);
      ctx.moveTo(x, area.top);
      ctx.lineTo(x, area.bottom);
      ctx.stroke();
      ctx.setLineDash([]);

      // Draw smaller steps first so the largest one stays on top
      [...group.steps].reverse().forEach(step => {
        const color = colorOf(step.joint);
        if (opts.metric === 'acceleration') {
          // Vertical edge from the left limit (open circle) to the right limit (filled dot)
          const y0 = clampY(yAxis.getPixelForValue(step.before));
          const y1 = clampY(yAxis.getPixelForValue(step.after));
          ctx.beginPath();
          ctx.strokeStyle = color;
          ctx.lineWidth = 3;
          ctx.moveTo(x, y0);
          ctx.lineTo(x, y1);
          ctx.stroke();
          ctx.beginPath();
          ctx.arc(x, y0, 3.5, 0, 2 * Math.PI);
          ctx.fillStyle = '#0a0c16';
          ctx.fill();
          ctx.lineWidth = 1.5;
          ctx.stroke();
          ctx.beginPath();
          ctx.arc(x, y1, 3.5, 0, 2 * Math.PI);
          ctx.fillStyle = color;
          ctx.fill();
        } else {
          // Jerk impulse: arrow from zero, length proportional to the step size
          const base = clampY(yAxis.getPixelForValue(0));
          const room = (step.step > 0 ? base - area.top : area.bottom - base) - 4;
          const len = Math.max(10, Math.min(room, 0.45 * (area.bottom - area.top)) * Math.abs(step.step) / maxStep);
          const tip = step.step > 0 ? base - len : base + len;
          const dir = step.step > 0 ? 1 : -1;
          ctx.beginPath();
          ctx.strokeStyle = color;
          ctx.lineWidth = 2.5;
          ctx.moveTo(x, base);
          ctx.lineTo(x, tip + dir * 5);
          ctx.stroke();
          ctx.beginPath();
          ctx.fillStyle = color;
          ctx.moveTo(x, tip);
          ctx.lineTo(x - 4.5, tip + dir * 7);
          ctx.lineTo(x + 4.5, tip + dir * 7);
          ctx.closePath();
          ctx.fill();
        }
      });

      // Label: time, kind and the largest steps of this group
      const maxLines = 4;
      const shown = group.steps.slice(0, maxLines);
      const lines = [{ text: `Δa @ ${group.t.toFixed(3)} s · ${STEP_KIND_LABELS[group.kind] || group.kind}`, color: '#e2e8f0' }];
      shown.forEach(step => {
        const sign = step.step > 0 ? '+' : '−';
        lines.push({ text: `J${step.joint + 1} ${sign}${Math.abs(step.step).toFixed(2)} rad/s²`, color: colorOf(step.joint) });
      });
      if (group.steps.length > shown.length) {
        lines.push({ text: `+${group.steps.length - shown.length} smaller`, color: '#94a3b8' });
      }
      ctx.font = '9px "JetBrains Mono", monospace';
      const lineH = 11;
      const w = Math.max(...lines.map(l => ctx.measureText(l.text).width)) + 8;
      const h = lines.length * lineH + 4;
      let bx = x + 6;
      if (bx + w > area.right) bx = x - 6 - w;
      bx = Math.max(area.left, bx);
      let by = area.top + 2;
      // Stack below any label box this one would overlap
      let moved = true;
      while (moved) {
        moved = false;
        for (const b of labelBoxes) {
          if (bx < b.x + b.w && bx + w > b.x && by < b.y + b.h && by + h > b.y) {
            by = b.y + b.h + 2;
            moved = true;
          }
        }
      }
      labelBoxes.push({ x: bx, y: by, w, h });
      ctx.fillStyle = 'rgba(10, 12, 22, 0.85)';
      ctx.fillRect(bx, by, w, h);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
      ctx.lineWidth = 1;
      ctx.strokeRect(bx, by, w, h);
      lines.forEach((l, i) => {
        ctx.fillStyle = l.color;
        ctx.fillText(l.text, bx + 4, by + 2 + (i + 1) * lineH - 2);
      });
    });
    ctx.restore();
  }
};

// Register custom plugins
Chart.register(verticalCursorPlugin, alignSliderPlugin, horizontalLimitsPlugin, accelerationStepsPlugin);

export class TrajectoryChart {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.chart = null;
    
    // Consistent color coding for joints J1..J6 (cycled if a robot has more joints)
    this.jointColors = [
      '#a855f7', // J1 Purple
      '#3b82f6', // J2 Blue
      '#14b8a6', // J3 Teal
      '#22c55e', // J4 Green
      '#f59e0b', // J5 Amber
      '#f43f5e'  // J6 Rose
    ];
    
    this.currentMetric = 'position'; // Default
    this.activeTrajData = null;
    this.cursorTime = 0.0;
    
    this.init();
  }
  
  init() {
    const ctx = this.canvas.getContext('2d');
    
    // Create empty chart initially
    this.chart = new Chart(ctx, {
      type: 'line',
      data: {
        datasets: []
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false, // Turn off transitions for raw speed
        elements: {
          point: { radius: 0 }, // Hide points, only show lines
          line: { borderDelta: 0, tension: 0, borderWidth: 1.8 } // straight segments: knots carry exact steps
        },
        layout: {
          padding: {
            left: 2,
            right: 8,
            top: 8,
            bottom: 44
          }
        },
        scales: {
          x: {
            type: 'linear',
            title: {
              display: false
            },
            grid: { color: 'rgba(255, 255, 255, 0.03)' },
            ticks: { color: '#94a3b8', font: { size: 9 } }
          },
          y: {
            title: {
              display: false,
              text: '',
              color: '#94a3b8',
              font: { size: 10, family: 'Inter' }
            },
            grid: { color: 'rgba(255, 255, 255, 0.03)' },
            ticks: { color: '#94a3b8', font: { size: 9 } }
          }
        },
        plugins: {
          legend: { display: false }, // Custom legend used in UI
          tooltip: {
            enabled: true,
            mode: 'index',
            intersect: false,
            backgroundColor: 'rgba(10, 12, 22, 0.95)',
            titleColor: '#22d3ee',
            titleFont: { family: 'JetBrains Mono', size: 10 },
            bodyFont: { family: 'Inter', size: 11 },
            borderWidth: 1,
            borderColor: 'rgba(255, 255, 255, 0.08)',
            callbacks: {
              title: (context) => `Time: ${context[0].parsed.x.toFixed(3)}s`
            }
          },
          verticalCursor: {
            timeVal: 0.0 // Value managed by app
          },
          horizontalLimits: {
            lines: [] // List of active limit lines to draw
          },
          accelerationSteps: {
            metric: null,
            groups: [], // Acceleration steps grouped by time
            colors: this.jointColors // plain data: Chart.js would call a function option as scriptable
          }
        }
      }
    });
  }
  
  /**
   * Evaluates the active trajectory splines and updates chart lines
   * @param {Object} trajData - Spline trajectory JSON data
   * @param {string} metric - 'position', 'velocity', 'acceleration', 'jerk'
   * @param {Object} [reprData] - Optional robot representation configuration for limits
   */
  update(trajData, metric = 'position', reprData = null) {
    this.activeTrajData = trajData;
    this.currentMetric = metric;
    
    if (!trajData) {
      this.clear();
      return;
    }
    
    // 1. Get trajectory duration
    let duration = 0.0;
    if (trajData.status === 70 && trajData.parts && trajData.parts.length > 0) {
      const lastPart = trajData.parts[trajData.parts.length - 1];
      const knots = lastPart.knots;
      if (knots && knots.length > 0) {
        duration = knots[knots.length - 1];
      }
    }
    
    // Fallback if it is a failed or static pose trajectory (duration = 0)
    if (duration === 0.0) {
      this.showStaticPlot(trajData, metric, reprData);
      return;
    }
    
    // 2. Sample every knot (both sides) plus a dense grid; jerk as exact steps
    const datasetsData = buildMetricSeries(trajData, metric);
    this.chart.data.datasets = this.makeDatasets(datasetsData);

    // 3. Mark acceleration steps (jerk impulses) at knots and part junctions
    this.stepGroups = groupStepsByTime(detectAccelerationSteps(trajData));
    this.chart.options.plugins.accelerationSteps.metric = metric;
    this.chart.options.plugins.accelerationSteps.groups = this.stepGroups;

    this.chart.options.scales.x.max = duration;
    this.chart.options.scales.x.min = 0;
    
    this.checkHorizontalLimits(datasetsData, metric, reprData);
    this.chart.update('none'); // Update immediately without animation
  }
  
  /**
   * Show horizontal curves for static pose trajectories
   * @param {Object} trajData - Spline trajectory JSON data
   * @param {string} metric - 'position', 'velocity', 'acceleration', 'jerk'
   * @param {Object} [reprData] - Optional robot representation configuration for limits
   */
  showStaticPlot(trajData, metric, reprData = null) {
    const numJoints = getJointCount(trajData);
    const targetState = trajData.targetState || new Array(numJoints).fill(0);
    
    const datasetsData = Array.from({ length: numJoints }, () => []);
    const timeSteps = [0.0, 1.0]; // Simple flat 0 to 1 seconds line
    
    timeSteps.forEach(t => {
      for (let j = 0; j < numJoints; j++) {
        let val = 0.0;
        if (metric === 'position') val = targetState[j];
        // Velocity, Acceleration, Jerk are zero for static states
        datasetsData[j].push({ x: t, y: val });
      }
    });
    
    this.chart.data.datasets = this.makeDatasets(datasetsData);
    this.stepGroups = [];
    this.chart.options.plugins.accelerationSteps.groups = [];
    
    this.chart.options.scales.x.max = 1.0;
    this.chart.options.scales.x.min = 0.0;
    
    this.checkHorizontalLimits(datasetsData, metric, reprData);
    this.chart.update('none');
  }

  jointColor(joint) {
    return this.jointColors[joint % this.jointColors.length];
  }

  makeDatasets(datasetsData) {
    return datasetsData.map((dataPoints, jIdx) => ({
      label: `Joint J${jIdx + 1}`,
      data: dataPoints,
      borderColor: this.jointColor(jIdx),
      backgroundColor: 'transparent',
      borderWidth: 1.8,
      pointRadius: 0,
      fill: false
    }));
  }

  /**
   * Helper to check if any joint value is within 5% of limits and setup limit lines
   */
  checkHorizontalLimits(datasetsData, metric, reprData) {
    const activeLines = [];
    if (reprData && datasetsData && (metric === 'position' || metric === 'velocity')) {
      const equipment = reprData.equipment_model || {};
      const limits = equipment.range_limits || [];
      const modelName = equipment.model_name || 'generic';
      const speedLimits = this.getRobotSpeedLimits(modelName, equipment);
      
      for (let j = 0; j < datasetsData.length; j++) {
        const curvePoints = datasetsData[j];
        if (!curvePoints || curvePoints.length === 0) continue;
        
        const yVals = curvePoints.map(pt => pt.y);
        const minCurveY = Math.min(...yVals);
        const maxCurveY = Math.max(...yVals);
        const jColor = this.jointColor(j);
        
        if (metric === 'position') {
          const limit = limits.find(l => l.joint_id === j);
          if (limit) {
            const minVal = limit.min_value;
            const maxVal = limit.max_value;
            const range = maxVal - minVal;
            
            // Check min limit
            if (minCurveY < minVal) {
              const label = `J${j+1} Min Limit EXCEEDED!`;
              if (!activeLines.some(l => Math.abs(l.value - minVal) < 1e-4)) {
                activeLines.push({ value: minVal, label: label, color: '#ef4444', width: 3.0, dash: [] });
              }
            } else if (minCurveY - minVal <= 0.05 * range) {
              const minDistVal = minCurveY - minVal;
              const ratio = Math.max(0, Math.min(1, (0.05 * range - minDistVal) / (0.05 * range)));
              const thickness = 1.0 + ratio * 1.5;
              const label = `J${j+1} Min Limit: ${(minVal * 180 / Math.PI).toFixed(0)}°`;
              if (!activeLines.some(l => Math.abs(l.value - minVal) < 1e-4)) {
                activeLines.push({ value: minVal, label: label, color: jColor, width: thickness, dash: [4, 4] });
              }
            }
            
            // Check max limit
            if (maxCurveY > maxVal) {
              const label = `J${j+1} Max Limit EXCEEDED!`;
              if (!activeLines.some(l => Math.abs(l.value - maxVal) < 1e-4)) {
                activeLines.push({ value: maxVal, label: label, color: '#ef4444', width: 3.0, dash: [] });
              }
            } else if (maxVal - maxCurveY <= 0.05 * range) {
              const minDistVal = maxVal - maxCurveY;
              const ratio = Math.max(0, Math.min(1, (0.05 * range - minDistVal) / (0.05 * range)));
              const thickness = 1.0 + ratio * 1.5;
              const label = `J${j+1} Max Limit: ${(maxVal * 180 / Math.PI).toFixed(0)}°`;
              if (!activeLines.some(l => Math.abs(l.value - maxVal) < 1e-4)) {
                activeLines.push({ value: maxVal, label: label, color: jColor, width: thickness, dash: [4, 4] });
              }
            }
          }
        } else if (metric === 'velocity') {
          const maxSpeed = speedLimits[j];
          if (maxSpeed) {
            const minVal = -maxSpeed;
            const maxVal = maxSpeed;
            
            // Check min limit
            if (minCurveY < minVal) {
              const label = `J${j+1} Speed Limit EXCEEDED!`;
              if (!activeLines.some(l => Math.abs(l.value - minVal) < 1e-4)) {
                activeLines.push({ value: minVal, label: label, color: '#ef4444', width: 3.0, dash: [] });
              }
            } else if (minCurveY - minVal <= 0.05 * maxSpeed) {
              const minDistVal = minCurveY - minVal;
              const ratio = Math.max(0, Math.min(1, (0.05 * maxSpeed - minDistVal) / (0.05 * maxSpeed)));
              const thickness = 1.0 + ratio * 1.5;
              const label = `J${j+1} Speed Limit: -${(maxSpeed * 180 / Math.PI).toFixed(0)}°/s`;
              if (!activeLines.some(l => Math.abs(l.value - minVal) < 1e-4)) {
                activeLines.push({ value: minVal, label: label, color: jColor, width: thickness, dash: [4, 4] });
              }
            }
            
            // Check max limit
            if (maxCurveY > maxVal) {
              const label = `J${j+1} Speed Limit EXCEEDED!`;
              if (!activeLines.some(l => Math.abs(l.value - maxVal) < 1e-4)) {
                activeLines.push({ value: maxVal, label: label, color: '#ef4444', width: 3.0, dash: [] });
              }
            } else if (maxVal - maxCurveY <= 0.05 * maxSpeed) {
              const minDistVal = maxVal - maxCurveY;
              const ratio = Math.max(0, Math.min(1, (0.05 * maxSpeed - minDistVal) / (0.05 * maxSpeed)));
              const thickness = 1.0 + ratio * 1.5;
              const label = `J${j+1} Speed Limit: ${(maxSpeed * 180 / Math.PI).toFixed(0)}°/s`;
              if (!activeLines.some(l => Math.abs(l.value - maxVal) < 1e-4)) {
                activeLines.push({ value: maxVal, label: label, color: jColor, width: thickness, dash: [4, 4] });
              }
            }
          }
        }
      }
    }
    
    // Configure limit lines plugin options
    if (!this.chart.options.plugins.horizontalLimits) {
      this.chart.options.plugins.horizontalLimits = {};
    }
    this.chart.options.plugins.horizontalLimits.lines = activeLines;

    // Adjust Y axis scale boundaries to ensure limit lines are fully visible
    delete this.chart.options.scales.y.min;
    delete this.chart.options.scales.y.max;
    
    if (activeLines.length > 0 && datasetsData) {
      let minY = Infinity;
      let maxY = -Infinity;
      for (let j = 0; j < datasetsData.length; j++) {
        if (datasetsData[j]) {
          datasetsData[j].forEach(pt => {
            if (pt.y < minY) minY = pt.y;
            if (pt.y > maxY) maxY = pt.y;
          });
        }
      }
      activeLines.forEach(line => {
        if (line.value < minY) minY = line.value;
        if (line.value > maxY) maxY = line.value;
      });
      const padding = (maxY - minY) * 0.08 || 0.1; // 8% padding to show text/lines comfortably
      this.chart.options.scales.y.min = minY - padding;
      this.chart.options.scales.y.max = maxY + padding;
    }
  }

  /**
   * Retrieves maximum velocity limits (radians/second) for each joint
   */
  getRobotSpeedLimits(modelName, equipmentModel = null) {
    if (equipmentModel && Array.isArray(equipmentModel.max_velocity) && equipmentModel.max_velocity.length > 0) {
      return equipmentModel.max_velocity;
    }
    const name = (modelName || '').toLowerCase();
    if (name.includes('h2017') || name.includes('doosan-h2017') || (name.includes('doosan') && !name.includes('p3020'))) {
      // Doosan H2017 J1: 100°/s, J2: 80°/s, J3: 100°/s, J4-J6: 180°/s
      return [
        100 * Math.PI / 180,
        80 * Math.PI / 180,
        100 * Math.PI / 180,
        180 * Math.PI / 180,
        180 * Math.PI / 180,
        180 * Math.PI / 180
      ];
    } else if (name.includes('p3020') || name.includes('doosan-p3020')) {
      // Doosan P3020 (5-DOF) J1: 100°/s, J2-J3: 80°/s, J4: 200°/s, J5: 360°/s
      return [
        100 * Math.PI / 180,
        80 * Math.PI / 180,
        80 * Math.PI / 180,
        200 * Math.PI / 180,
        360 * Math.PI / 180
      ];
    } else if (name.includes('cr20a') || name.includes('cr20')) {
      // CR20A J1-J2: 120°/s, J3: 150°/s, J4-J6: 180°/s
      return [
        120 * Math.PI / 180,
        120 * Math.PI / 180,
        150 * Math.PI / 180,
        180 * Math.PI / 180,
        180 * Math.PI / 180,
        180 * Math.PI / 180
      ];
    } else if (name.includes('cr30') || name.includes('dobot')) {
      // CR30H J1-J2: 150°/s, J3: 200°/s, J4-J6: 300°/s
      return [
        150 * Math.PI / 180,
        150 * Math.PI / 180,
        200 * Math.PI / 180,
        300 * Math.PI / 180,
        300 * Math.PI / 180,
        300 * Math.PI / 180
      ];
    } else if (name.includes('aubo-is25') || name.includes('is25')) {
      // Aubo iS25 standard velocity limits
      return [
        2.5831,
        2.5831,
        3.1067,
        5.1662,
        5.1662,
        5.1662
      ];
    } else {
      // Standard default collaborative robot speed limits: 150°/s
      return Array(6).fill(150 * Math.PI / 180);
    }
  }
  
  /**
   * Sets the timeline cursor position on the graph
   * @param {number} timeVal - Playback time in seconds
   */
  setCursor(timeVal) {
    this.cursorTime = timeVal;
    if (this.chart && this.chart.options.plugins.verticalCursor) {
      this.chart.options.plugins.verticalCursor.timeVal = timeVal;
      this.chart.update('none'); // Update line quickly
    }
  }
  
  clear() {
    this.chart.data.datasets = [];
    this.chart.update('none');
  }
}
