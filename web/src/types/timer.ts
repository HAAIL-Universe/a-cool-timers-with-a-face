/**
 * Timer domain types for frontend state and API contracts.
 */

/**
 * Urgency level affecting visual feedback.
 */
export type UrgencyLevel = 'low' | 'medium' | 'high' | 'critical';

/**
 * 8-bit LED-style facial expression reflecting urgency.
 */
export type FacialExpression = 'neutral' | 'concerned' | 'worried' | 'alarm';

/**
 * Colour intensity mapping urgency to visual feedback.
 */
export interface ColourIntensity {
  red: number;
  green: number;
  blue: number;
}

/**
 * Core timer data from API.
 */
export interface Timer {
  id: string;
  initialDuration: number;
  remainingTime: number;
  createdAt: string;
  startedAt: string;
  status: 'running' | 'paused' | 'expired';
}

/**
 * Complete timer UI state including urgency and visual feedback.
 */
export interface TimerState {
  timer: Timer;
  urgencyLevel: UrgencyLevel;
  colourIntensity: ColourIntensity;
  facialExpression: FacialExpression;
  isRunning: boolean;
  isExpired: boolean;
  remainingPercentage: number;
  status: 'running' | 'paused' | 'expired';
}
