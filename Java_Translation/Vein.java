import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class Vein
    extends NotAnimated
{
    protected int resource_distance = 1;
    public Vein (String name, /*ArrayList imgs,*/ Point position, int rate,
                 int resource_distance)
        {
        super (name, /*imgs,*/ position, rate);
        this.resource_distance = resource_distance;
    }
    public int get_resource_distance ()
    {
        return resource_distance;
    }
    public String entity_string ()
    {
        return ("vein" + name + (position.xCoor()) + (position.yCoor()) +(rate) +
                (resource_distance));
    }
}
