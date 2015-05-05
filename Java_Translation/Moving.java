import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class Moving
    extends Entity
{
    protected int animation_rate;

    public Moving (String name, Point position, /*ArrayList imgs,*/ int animation_rate)
    {
        super (name,/* imgs,*/ position);
        this.animation_rate = animation_rate;
    }
    public int get_animation_rate ()
    {
        return animation_rate;
    }
    //public void next_image()
    {
        //current_img = (current_img + 1) % (imgs.size());
    }
}
