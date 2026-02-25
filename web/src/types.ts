/**
 * Urgency level enumeration for timer state.
 */
export type UrgencyLevel = 'calm' | 'anxious' | 'alarm';

/**
 * Facial expression state.
 */
export type FacialState = 'calm' | 'anxious' | 'alarm' | 'defeated';

/**
 * Timer status enumeration.
 */
export type TimerStatus = 'idle' | 'running' | 'paused' | 'expired';

/**
 * Main timer state object returned by backend and used in frontend.
 */
export interface TimerState {
  countdown: number;
  duration: number;
  is_paused: boolean;
  is_expired: boolean;
  urgency_level: UrgencyLevel;
  colour_intensity: number;
  last_reset_at: string | null;
}

/**
 * Urgency state derived from timer state.
 */
export interface UrgencyState {
  urgency_level: UrgencyLevel;
  colour_intensity: number;
  remaining_percent: number;
  facial_expression: FacialState;
}

/**
 * Configuration for setting timer duration.
 */
export interface TimerConfig {
  duration: number;
}

/**
 * Request body for configuring timer.
 */
export interface TimerConfigRequest {
  duration: number;
}

/**
 * Response from /timers/get endpoint.
 */
export interface TimerResponse {
  countdown: number;
  duration: number;
  is_paused: boolean;
  is_expired: boolean;
  urgency_level: UrgencyLevel;
  colour_intensity: number;
  last_reset_at: string | null;
}

/**
 * Response from /urgency/get endpoint.
 */
export interface UrgencyResponse {
  urgency_level: UrgencyLevel;
  colour_intensity: number;
  remaining_percent: number;
  facial_expression: FacialState;
}

/**
 * Timer event types.
 */
export type TimerEventType = 'start' | 'pause' | 'resume' | 'reset' | 'configure' | 'expire';

/**
 * Timer event record.
 */
export interface TimerEvent {
  id: string;
  event_type: TimerEventType;
  timestamp: string;
  timer_state: TimerState;
}

/**
 * Generic API error response.
 */
export interface ApiError {
  detail: string;
}

/**
 * Preset timer durations (in seconds).
 */
export const TIMER_PRESETS = {
  '30 seconds': 30,
  '1 minute': 60,
  '5 minutes': 300,
  '10 minutes': 600,
  '30 minutes': 1800,
  '1 hour': 3600,
  '90 seconds': 90,
} as const;

export type PresetLabel = keyof typeof TIMER_PRESETS;

/**
 * Urgency thresholds as percentages (0-100).
 */
export const URGENCY_THRESHOLDS = {
  calm: 50,
  anxious: 25,
  alarm: 0,
} as const;

/**
 * Colour mapping for urgency levels.
 */
export const URGENCY_COLOURS = {
  calm: '#00AA00',
  anxious: '#FFAA00',
  alarm: '#AA0000',
} as const;
