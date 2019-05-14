/**
 * Defines all controllable parameters.
 *
 * @author Wenzhou Wei (Initial Design), Dafu Ai
 */
class Params {
    /**
     * Factor for determining arrest probability.
     */
    static final double K = 2.3;

    /**
     * By how much must G > N to make someone rebel?
     */
    static final double THRESHOLD = 0.1;

    /**
     * Width of the patch map (i.e. the number of patches in x direction).
     */
    static final int MAP_WIDTH = 5;

    /**
     * Width of the patch map (i.e. the number of patches in x direction).
     */
    static final int MAP_HEIGHT = 5;

    /**
     * Percentage of cops (in the total number of patches in the map).
     */
    private static final double INITIAL_COP_DENSITY = 0.04;

    /**
     * Percentage of agents (in the total number of patches in the map).
     */
    private static final double INITIAL_AGENT_DENSITY = 0.700;

    /**
     * Defines the radius of neighbourhood for any patch.
     */
    static final double VISION = 7.0;

    /**
     * Maximum possible jailed term.
     */
    static final int MAX_JAILED_TERM = 30;

    /**
     * Government legitimacy
     *
     * @ TODO: 14/5/19 make this dynamic
     */
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
