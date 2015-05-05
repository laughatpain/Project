import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class Grid
{
    protected int width;
    protected int height;
    protected WorldObject[][] cells;

    public Grid (int width, int height, WorldObject occupancy_value)
    {
        this.width = width;
        this.height = height;
        this.cells = new WorldObject[height][width];

        for (int row =0; row<height; row++)
        {
            for (int column=0; column< width; column++)
            {
                 cells[row][column] = (occupancy_value);
            }
        }
    }
    public void set_cell (Point point, WorldObject value)
    {
        cells [point.yCoor()][point.xCoor()] = value;
    }
    public WorldObject get_cell (Point point)
    {
        return cells [point.yCoor()][point.xCoor()];
    }

}
