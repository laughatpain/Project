import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class Blacksmith
    extends Entity
{
    protected int resource_limit;
    protected int rate;
    protected int resource_distance = 1;
    public Blacksmith (String name, /*ArrayList imgs,*/ Point position, int rate,
                       int resource_distance, int resource_limit)
    {
        super (name, /*imgs,*/ position);
        this.rate = rate;
        this.resource_distance = resource_distance;
        this.resource_limit = resource_limit;
    }
    public String entity_string ()
    {
        return ("blacksmith" + name + position.xCoor() + position.yCoor() + resource_limit + rate
        + resource_distance);
    }
}

