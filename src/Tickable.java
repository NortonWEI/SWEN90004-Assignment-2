/**
 * By 'tickable', we mean this class has a state and for each time tick, we should let this class perform update.
 */
public interface Tickable {
    /**
     * Perform update on its current state.
     */
    void update();
}
