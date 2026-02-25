import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useTimer } from '../hooks/useTimer';
import * as api from '../api';
import { TimerState, UrgencyState } from '../types';

vi.mock('../api');

const mockTimerState: TimerState = {
  countdown: 60,
  duration: 60,
  is_paused: false,
  is_expired: false,
  urgency_level: 'calm',
  colour_intensity: 0.1,
  last_reset_at: null,
};

const mockUrgencyState: UrgencyState = {
  urgency_level: 'calm',
  colour_intensity: 0.1,
  remaining_percent: 100,
  facial_expression: 'calm',
};

describe('useTimer', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('initializes with null state and loads timer on mount', async () => {
    vi.mocked(api.getTimerState).mockResolvedValue({
      ...mockTimerState,
      urgency_level: 'calm',
    });

    const { result } = renderHook(() => useTimer());

    expect(result.current.timerState).toBeNull();
    expect(result.current.isLoading).toBe(true);

    await waitFor(() => {
      expect(result.current.timerState).not.toBeNull();
    });

    expect(result.current.timerState?.countdown).toBe(60);
    expect(result.current.urgencyState?.urgency_level).toBe('calm');
    expect(result.current.isLoading).toBe(false);
  });

  it('sets facial state from urgency state', async () => {
    vi.mocked(api.getTimerState).mockResolvedValue({
      ...mockTimerState,
      urgency_level: 'alarm',
    });

    const { result } = renderHook(() => useTimer());

    await waitFor(() => {
      expect(result.current.facialState).toBe('alarm');
    });
  });

  it('defaults facial state to calm when urgency is null', async () => {
    vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);

    const { result } = renderHook(() => useTimer());

    await waitFor(() => {
      expect(result.current.timerState).not.toBeNull();
    });

    expect(result.current.facialState).toBe('calm');
  });

  describe('polling', () => {
    it('polls timer state every 1000ms', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      const initialCallCount = vi.mocked(api.getTimerState).mock.calls.length;

      act(() => {
        vi.advanceTimersByTime(1000);
      });

      await waitFor(() => {
        expect(vi.mocked(api.getTimerState).mock.calls.length).toBeGreaterThan(
          initialCallCount
        );
      });
    });

    it('updates countdown on each poll', async () => {
      vi.mocked(api.getTimerState)
        .mockResolvedValueOnce({ ...mockTimerState, countdown: 60 })
        .mockResolvedValueOnce({ ...mockTimerState, countdown: 59 })
        .mockResolvedValue({ ...mockTimerState, countdown: 58 });

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState?.countdown).toBe(60);
      });

      act(() => {
        vi.advanceTimersByTime(1000);
      });

      await waitFor(() => {
        expect(result.current.timerState?.countdown).toBe(59);
      });

      act(() => {
        vi.advanceTimersByTime(1000);
      });

      await waitFor(() => {
        expect(result.current.timerState?.countdown).toBe(58);
      });
    });

    it('continues polling until unmount', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);

      const { result, unmount } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      const callCountBefore = vi.mocked(api.getTimerState).mock.calls.length;

      unmount();

      act(() => {
        vi.advanceTimersByTime(2000);
      });

      const callCountAfter = vi.mocked(api.getTimerState).mock.calls.length;
      expect(callCountAfter).toBe(callCountBefore);
    });
  });

  describe('configure', () => {
    it('calls configureTimer API with duration', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.configureTimer).mockResolvedValue({
        ...mockTimerState,
        duration: 90,
        countdown: 90,
      });

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.configure(90);
      });

      expect(vi.mocked(api.configureTimer)).toHaveBeenCalledWith(90);
    });

    it('persists duration to localStorage', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.configureTimer).mockResolvedValue({
        ...mockTimerState,
        duration: 300,
      });

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.configure(300);
      });

      expect(localStorage.getItem('timer_duration')).toBe('300');
    });

    it('refetches state after configure', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.configureTimer).mockResolvedValue({
        ...mockTimerState,
        duration: 120,
      });

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      const getCallsBefore = vi.mocked(api.getTimerState).mock.calls.length;

      await act(async () => {
        await result.current.configure(120);
      });

      expect(vi.mocked(api.getTimerState).mock.calls.length).toBeGreaterThan(
        getCallsBefore
      );
    });

    it('sets isLoading to true during configure', async () => {
      let resolveConfig: (value: TimerState) => void;
      const configPromise = new Promise<TimerState>(resolve => {
        resolveConfig = resolve;
      });

      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.configureTimer).mockReturnValue(configPromise);

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      let isLoadingDuringConfigure = false;

      act(() => {
        result.current.configure(90).then(() => {
          // promise settled
        });
        isLoadingDuringConfigure = result.current.isLoading;
      });

      expect(isLoadingDuringConfigure).toBe(true);

      await act(async () => {
        resolveConfig!({ ...mockTimerState, duration: 90 });
      });

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });
    });

    it('handles configure errors gracefully', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.configureTimer).mockRejectedValue(
        new Error('Configure failed')
      );

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.configure(90);
      });

      expect(result.current.error).toBe('Configure failed');
    });

    it('clears error on successful configure', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.configureTimer).mockResolvedValue({
        ...mockTimerState,
        duration: 90,
      });

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.configure(90);
      });

      expect(result.current.error).toBeNull();
    });
  });

  describe('reset', () => {
    it('calls resetTimer API', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.resetTimer).mockResolvedValue(mockTimerState);

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.reset();
      });

      expect(vi.mocked(api.resetTimer)).toHaveBeenCalled();
    });

    it('refetches state after reset', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.resetTimer).mockResolvedValue(mockTimerState);

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      const getCallsBefore = vi.mocked(api.getTimerState).mock.calls.length;

      await act(async () => {
        await result.current.reset();
      });

      expect(vi.mocked(api.getTimerState).mock.calls.length).toBeGreaterThan(
        getCallsBefore
      );
    });

    it('handles reset errors gracefully', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.resetTimer).mockRejectedValue(new Error('Reset failed'));

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.reset();
      });

      expect(result.current.error).toBe('Reset failed');
    });
  });

  describe('pause', () => {
    it('calls pauseTimer API', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.pauseTimer).mockResolvedValue({
        ...mockTimerState,
        is_paused: true,
      });

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.pause();
      });

      expect(vi.mocked(api.pauseTimer)).toHaveBeenCalled();
    });

    it('refetches state after pause', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.pauseTimer).mockResolvedValue({
        ...mockTimerState,
        is_paused: true,
      });

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      const getCallsBefore = vi.mocked(api.getTimerState).mock.calls.length;

      await act(async () => {
        await result.current.pause();
      });

      expect(vi.mocked(api.getTimerState).mock.calls.length).toBeGreaterThan(
        getCallsBefore
      );
    });

    it('handles pause errors gracefully', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.pauseTimer).mockRejectedValue(new Error('Pause failed'));

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.pause();
      });

      expect(result.current.error).toBe('Pause failed');
    });
  });

  describe('resume', () => {
    it('calls resumeTimer API', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.resumeTimer).mockResolvedValue({
        ...mockTimerState,
        is_paused: false,
      });

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.resume();
      });

      expect(vi.mocked(api.resumeTimer)).toHaveBeenCalled();
    });

    it('refetches state after resume', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.resumeTimer).mockResolvedValue({
        ...mockTimerState,
        is_paused: false,
      });

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      const getCallsBefore = vi.mocked(api.getTimerState).mock.calls.length;

      await act(async () => {
        await result.current.resume();
      });

      expect(vi.mocked(api.getTimerState).mock.calls.length).toBeGreaterThan(
        getCallsBefore
      );
    });

    it('handles resume errors gracefully', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.resumeTimer).mockRejectedValue(new Error('Resume failed'));

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.resume();
      });

      expect(result.current.error).toBe('Resume failed');
    });
  });

  describe('localStorage persistence', () => {
    it('persists duration when configuring', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.configureTimer).mockResolvedValue({
        ...mockTimerState,
        duration: 1800,
      });

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.configure(1800);
      });

      expect(localStorage.getItem('timer_duration')).toBe('1800');
    });

    it('persists multiple durations across calls', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.configureTimer).mockResolvedValue(mockTimerState);

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.configure(60);
      });
      expect(localStorage.getItem('timer_duration')).toBe('60');

      await act(async () => {
        await result.current.configure(300);
      });
      expect(localStorage.getItem('timer_duration')).toBe('300');
    });

    it('stores duration as string in localStorage', async () => {
      vi.mocked(api.getTimerState).mockResolvedValue(mockTimerState);
      vi.mocked(api.configureTimer).mockResolvedValue({
        ...mockTimerState,
        duration: 90,
      });

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.timerState).not.toBeNull();
      });

      await act(async () => {
        await result.current.configure(90);
      });

      const stored = localStorage.getItem('timer_duration');
      expect(typeof stored).toBe('string');
      expect(stored).toBe('90');
    });
  });

  describe('error handling', () => {
    it('clears error when fetch succeeds', async () => {
      vi.mocked(api.getTimerState)
        .mockRejectedValueOnce(new Error('Network error'))
        .mockResolvedValue(mockTimerState);

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.error).toBe('Network error');
      });

      act(() => {
        vi.advanceTimersByTime(1000);
      });

      await waitFor(() => {
        expect(result.current.error).toBeNull();
      });
    });

    it('converts Error objects to message string', async () => {
      vi.mocked(api.getTimerState).mockRejectedValue(
        new Error('Test error message')
      );

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.error).toBe('Test error message');
      });
    });

    it('handles non-Error objects as Unknown error', async () => {
      vi.mocked(api.getTimerState).mockRejectedValue('string error');

      const { result } = renderHook(() => useTimer());

      await waitFor(() => {
        expect(result.current.error).toBe('Unknown error');
      });
    });
  });
});
