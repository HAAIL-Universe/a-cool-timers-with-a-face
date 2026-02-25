import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import TimerDisplay from '../components/TimerDisplay';
import { TimerState } from '../types/timer';

describe('TimerDisplay', () => {
  it('renders --:-- when timerState is null', () => {
    render(<TimerDisplay timerState={null} />);
    expect(screen.getByText('--:--')).toBeInTheDocument();
  });

  it('renders MM:SS format for valid time remaining', () => {
    const timerState: TimerState = {
      id: 'test-timer',
      status: 'active',
      initial_seconds: 60,
      remaining_seconds: 45,
      urgency_level: 'low',
      last_reset_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    render(<TimerDisplay timerState={timerState} />);
    expect(screen.getByText('00:45')).toBeInTheDocument();
  });

  it('renders 01:30 for 90 seconds remaining', () => {
    const timerState: TimerState = {
      id: 'test-timer',
      status: 'active',
      initial_seconds: 120,
      remaining_seconds: 90,
      urgency_level: 'low',
      last_reset_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    render(<TimerDisplay timerState={timerState} />);
    expect(screen.getByText('01:30')).toBeInTheDocument();
  });

  it('applies low urgency color (green) for safe zone', () => {
    const timerState: TimerState = {
      id: 'test-timer',
      status: 'active',
      initial_seconds: 100,
      remaining_seconds: 80,
      urgency_level: 'low',
      last_reset_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    const { container } = render(<TimerDisplay timerState={timerState} />);
    const displayElement = container.querySelector('.display');
    expect(displayElement).toHaveStyle({ color: '#00FF00' });
  });

  it('applies medium urgency color (yellow) for caution zone', () => {
    const timerState: TimerState = {
      id: 'test-timer',
      status: 'active',
      initial_seconds: 100,
      remaining_seconds: 40,
      urgency_level: 'medium',
      last_reset_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    const { container } = render(<TimerDisplay timerState={timerState} />);
    const displayElement = container.querySelector('.display');
    expect(displayElement).toHaveStyle({ color: '#FFFF00' });
  });

  it('applies high urgency color (orange) for urgent zone', () => {
    const timerState: TimerState = {
      id: 'test-timer',
      status: 'active',
      initial_seconds: 100,
      remaining_seconds: 15,
      urgency_level: 'high',
      last_reset_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    const { container } = render(<TimerDisplay timerState={timerState} />);
    const displayElement = container.querySelector('.display');
    expect(displayElement).toHaveStyle({ color: '#FF8800' });
  });

  it('applies critical urgency color (red) for critical zone', () => {
    const timerState: TimerState = {
      id: 'test-timer',
      status: 'active',
      initial_seconds: 100,
      remaining_seconds: 5,
      urgency_level: 'critical',
      last_reset_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    const { container } = render(<TimerDisplay timerState={timerState} />);
    const displayElement = container.querySelector('.display');
    expect(displayElement).toHaveStyle({ color: '#FF0000' });
  });

  it('renders 00:00 when remaining_seconds is 0', () => {
    const timerState: TimerState = {
      id: 'test-timer',
      status: 'expired',
      initial_seconds: 60,
      remaining_seconds: 0,
      urgency_level: 'critical',
      last_reset_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    render(<TimerDisplay timerState={timerState} />);
    expect(screen.getByText('00:00')).toBeInTheDocument();
  });

  it('applies text-shadow glow effect matching urgency color', () => {
    const timerState: TimerState = {
      id: 'test-timer',
      status: 'active',
      initial_seconds: 100,
      remaining_seconds: 50,
      urgency_level: 'low',
      last_reset_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    const { container } = render(<TimerDisplay timerState={timerState} />);
    const displayElement = container.querySelector('.display');
    expect(displayElement).toHaveStyle({ textShadow: '0 0 10px #00FF00' });
  });

  it('renders single digit seconds with leading zero', () => {
    const timerState: TimerState = {
      id: 'test-timer',
      status: 'active',
      initial_seconds: 60,
      remaining_seconds: 5,
      urgency_level: 'critical',
      last_reset_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    render(<TimerDisplay timerState={timerState} />);
    expect(screen.getByText('00:05')).toBeInTheDocument();
  });

  it('renders single digit minutes with leading zero', () => {
    const timerState: TimerState = {
      id: 'test-timer',
      status: 'active',
      initial_seconds: 600,
      remaining_seconds: 65,
      urgency_level: 'low',
      last_reset_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    render(<TimerDisplay timerState={timerState} />);
    expect(screen.getByText('01:05')).toBeInTheDocument();
  });
});
