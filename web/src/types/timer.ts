/**
 * Timer type definitions and interfaces
 */

export type TimerStatus = 'active' | 'paused' | 'expired' | 'completed';

export type UrgencyLevel = 'low' | 'medium' | 'high' | 'critical';

export type FacialExpression = 'calm' | 'concerned' | 'stressed' | 'critical';

export interface ColourIntensity {
  red: number;
  green: number;
  blue: number;
}

export interface Timer {
  id: string;
  initialSeconds: number;
  remainingSeconds: number;
  status: TimerStatus;
  urgencyLevel: UrgencyLevel;
  startedAt: string;
  lastResetAt: string;
  createdAt: string;
}

export interface TimerState {
  id: string;
  remainingTime: number;
  remainingPercentage: number;
  urgencyLevel: UrgencyLevel;
  colourIntensity: ColourIntensity;
  facialExpression: FacialExpression;
}

export interface TimerCreateRequest {
  duration: number;
}

export interface TimerSession {
  id: string;
  timerId: string;
  totalDurationSeconds: number;
  resetsCount: number;
  completedAt: string | null;
  createdAt: string;
}

export interface TimerEvent {
  id: string;
  timerId: string;
  eventType: string;
  urgencyLevel: UrgencyLevel | null;
  createdAt: string;
}
