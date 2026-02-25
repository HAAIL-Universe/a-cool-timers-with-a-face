import { Timer, TimerState } from '../types/timer';

const API_BASE_URL = '/api';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

export async function createTimer(durationSeconds: number): Promise<Timer> {
  const response = await fetch(`${API_BASE_URL}/timers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ duration_seconds: durationSeconds }),
  });
  return handleResponse<Timer>(response);
}

export async function getTimerState(timerId: string): Promise<TimerState> {
  const response = await fetch(`${API_BASE_URL}/timers/${timerId}/state`);
  return handleResponse<TimerState>(response);
}

export async function startTimer(timerId: string): Promise<TimerState> {
  const response = await fetch(`${API_BASE_URL}/timers/${timerId}/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<TimerState>(response);
}

export async function pauseTimer(timerId: string): Promise<TimerState> {
  const response = await fetch(`${API_BASE_URL}/timers/${timerId}/pause`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<TimerState>(response);
}

export async function resetTimer(timerId: string): Promise<TimerState> {
  const response = await fetch(`${API_BASE_URL}/timers/${timerId}/reset`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<TimerState>(response);
}

export async function deleteTimer(timerId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/timers/${timerId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
}
