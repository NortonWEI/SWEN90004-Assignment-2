public class Params {
    static final double K = 2.3;
    static final double THRESHOLD = 0.1;

    static final int MAP_WIDTH = 400;
    static final int MAP_HEIGHT = 400;
    static final double COP_DENSITY = 0.100;
    static final double AGENT_DENSITY = 0.700;
    static final double VISION = 7.0;
    static final int MAX_JAILED_TERM = 30;
    static final double GOVERNMENT_LEGITIMACY = 0.8;

    static private int NUM_PATCH() {
        return MAP_WIDTH * MAP_HEIGHT;
    }

    static int NUM_COP() {
        return (int) (NUM_PATCH() * COP_DENSITY);
    }

    static int NUM_AGENT() {
        return (int) (NUM_PATCH() * AGENT_DENSITY);
    }
}
