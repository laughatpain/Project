import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class Background
    extends WorldObject
{
    private String name;
   /* private ArrayList imgs;*/
    private int current_img;

    public Background (String name /*ArrayList imgs int current_img*/)
    {
        super (name /*imgs*/);
        this.current_img = 0;
    }
}

