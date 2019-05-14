/**
 * Defines all controllable parameters.
 */
class Params {
    static final double K = 2.3;
    static final double THRESHOLD = 0.1;
    static final int MAP_WIDTH = 5;
    static final int MAP_HEIGHT = 5;
    private static final double INITIAL_COP_DENSITY = 0.04;
    private static final double INITIAL_AGENT_DENSITY = 0.700;
    static final double VISION = 7.0;
    static final int MAX_JAILED_TERM = 30;
    static final double GOVERNMENT_LEGITIMACY = 0.82;

    /**
     * @return total number of patches
     */
    static int NUM_PATCH() {
        return MAP_WIDTH * MAP_HEIGHT;
    }

    /**
     * @return total number of cops
     */
    static int NUM_COP() {
        return (int) (NUM_PATCH() * INITIAL_COP_DENSITY);
    }

    /**
     * @return total number of agents
     */
    static int NUM_AGENT() {
        return (int) (NUM_PATCH() * INITIAL_AGENT_DENSITY);
    }
}
