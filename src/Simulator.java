public class Simulator {

    public static void main(String[] args) throws InterruptedException {
        Cop[] cops = new Cop[Params.NUM_COP()];
        Agent[] agents = new Agent[Params.NUM_AGENT()];
        Patch[][] map = new Patch[Params.MAP_WIDTH][Params.MAP_HEIGHT];

        for (int i = 0; i < Params.MAP_WIDTH; i++) {
            for (int j = 0; j < Params.MAP_HEIGHT; j++) {
                map[i][j] = new Patch(i + 0.5, j + 0.5);
            }
        }

        for (Cop cop : cops) {
            cop = new Cop();
            cop.start();
        }

        for (Agent agent : agents) {
            agent = new Agent();
            agent.start();
        }

        for (Cop cop : cops) {
            cop.join();
        }

        for (Agent agent : agents) {
            agent.join();
        }
    }
}
