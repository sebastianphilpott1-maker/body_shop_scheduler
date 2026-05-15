"""
controller.rolling_horizon
==========================

Top-level orchestration loop:

    while not done:
        scenario   = current_state(shop)
        model, h   = build_model(scenario)
        schedule   = solve(model, h)
        next_event = simulate_until_trigger(schedule, scenario)
        shop.commit_up_to(next_event.time)

Triggers for replanning include: kit late by more than threshold,
operator going home sick, process-time deviation above threshold.
"""

# TODO: run_rolling_horizon(scenario, config) -> History
