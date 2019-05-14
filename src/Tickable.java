/**
 * By 'tickable', we mean this class has a state and for each time tick, we should let this class perform update.
 *
 * @author Dafu Ai
 */
public interface Tickable {
    /**
     * Perform update on its current state.
     */
    void update();
}
