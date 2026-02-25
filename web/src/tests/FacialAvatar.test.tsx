import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import FacialAvatar from '../components/FacialAvatar';

describe('FacialAvatar', () => {
  it('renders with calm expression when expression prop is "calm"', () => {
    render(
      <FacialAvatar
        expression="calm"
        urgencyLevel="low"
        isPulsing={false}
      />
    );
    const container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('facial-avatar-calm');
  });

  it('renders with concerned expression when expression prop is "concerned"', () => {
    render(
      <FacialAvatar
        expression="concerned"
        urgencyLevel="medium"
        isPulsing={false}
      />
    );
    const container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('facial-avatar-concerned');
  });

  it('renders with stressed expression when expression prop is "stressed"', () => {
    render(
      <FacialAvatar
        expression="stressed"
        urgencyLevel="high"
        isPulsing={false}
      />
    );
    const container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('facial-avatar-stressed');
  });

  it('renders with critical expression when expression prop is "critical"', () => {
    render(
      <FacialAvatar
        expression="critical"
        urgencyLevel="critical"
        isPulsing={true}
      />
    );
    const container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('facial-avatar-critical');
  });

  it('applies pulse animation class only when isPulsing is true and urgencyLevel is critical', () => {
    const { rerender } = render(
      <FacialAvatar
        expression="critical"
        urgencyLevel="critical"
        isPulsing={false}
      />
    );
    let container = screen.getByTestId('facial-avatar');
    expect(container).not.toHaveClass('pulse-animation');

    rerender(
      <FacialAvatar
        expression="critical"
        urgencyLevel="critical"
        isPulsing={true}
      />
    );
    container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('pulse-animation');
  });

  it('does not apply pulse animation when isPulsing is true but urgencyLevel is not critical', () => {
    render(
      <FacialAvatar
        expression="stressed"
        urgencyLevel="high"
        isPulsing={true}
      />
    );
    const container = screen.getByTestId('facial-avatar');
    expect(container).not.toHaveClass('pulse-animation');
  });

  it('applies urgency tint class based on urgencyLevel prop', () => {
    const { rerender } = render(
      <FacialAvatar
        expression="calm"
        urgencyLevel="low"
        isPulsing={false}
      />
    );
    let container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('urgency-low');

    rerender(
      <FacialAvatar
        expression="concerned"
        urgencyLevel="medium"
        isPulsing={false}
      />
    );
    container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('urgency-medium');

    rerender(
      <FacialAvatar
        expression="stressed"
        urgencyLevel="high"
        isPulsing={false}
      />
    );
    container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('urgency-high');

    rerender(
      <FacialAvatar
        expression="critical"
        urgencyLevel="critical"
        isPulsing={false}
      />
    );
    container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('urgency-critical');
  });

  it('renders a 16x16 pixel grid container', () => {
    render(
      <FacialAvatar
        expression="calm"
        urgencyLevel="low"
        isPulsing={false}
      />
    );
    const grid = screen.getByTestId('pixel-grid');
    expect(grid).toBeInTheDocument();
    expect(grid).toHaveClass('pixel-grid-16x16');
  });

  it('updates expression class when expression prop changes', () => {
    const { rerender } = render(
      <FacialAvatar
        expression="calm"
        urgencyLevel="low"
        isPulsing={false}
      />
    );
    let container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('facial-avatar-calm');

    rerender(
      <FacialAvatar
        expression="concerned"
        urgencyLevel="low"
        isPulsing={false}
      />
    );
    container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('facial-avatar-concerned');
    expect(container).not.toHaveClass('facial-avatar-calm');
  });

  it('maintains all class combinations when multiple props change', () => {
    const { rerender } = render(
      <FacialAvatar
        expression="calm"
        urgencyLevel="low"
        isPulsing={false}
      />
    );
    let container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass('facial-avatar-calm', 'urgency-low');

    rerender(
      <FacialAvatar
        expression="critical"
        urgencyLevel="critical"
        isPulsing={true}
      />
    );
    container = screen.getByTestId('facial-avatar');
    expect(container).toHaveClass(
      'facial-avatar-critical',
      'urgency-critical',
      'pulse-animation'
    );
  });
});
