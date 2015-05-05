
import java.util.ArrayList;
import java.util.List;


/**
 * Created by James on 5/3/2015.
 */
public class Entity
    extends WorldObject
{
    protected String name;
    //protected ArrayList imgs;
    protected int current_img;
    protected Point position;
    protected ArrayList<String> pending_actions;

    public Entity (String name, /*ArrayList imgs,*/ Point position)
    {
        super(name /*imgs*/);
        this.position = position;
        this.pending_actions = new ArrayList<String>();

    }

    public Point get_position ()
    {
        return position;
    }
    //public ArrayList get_images ()
    {
        //return imgs;
    }
    public Point set_position (Point point)
    {
        return position = point;
    }
    public void remove_pending_actions (String action)
    {
        pending_actions.remove(action);
    }
    public void add_pending_actions ( String action)
    {
        pending_actions.add(action);
    }
    public ArrayList<String> get_pending_actions ()
    {
        return pending_actions;
    }
    public void clear_pending_actions ()
    {
       pending_actions = new ArrayList<String>();
    }
}

