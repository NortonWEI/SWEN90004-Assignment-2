public class Patch {

    private boolean isOccupied = false;
    private double x;
    private double y;

    public Patch(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public boolean isOccupied() {
        return isOccupied;
    }

    public void setOccupied(boolean occupied) {
        isOccupied = occupied;
    }
}
