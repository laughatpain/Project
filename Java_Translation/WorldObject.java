import java.util.ArrayList;

/**
 * Created by James on 5/4/2015.
 */
public class WorldObject
{
    private String name;
    //private ArrayList<Integer> imgs;
    private int current_img;

    public WorldObject (String name /*ArrayList imgs*/)
    {
        this.name = name;
        //this.imgs = imgs;
        this.current_img = 0;
    }
    //public int get_image()
    {
        //return imgs.get(current_img);
    }
    public String get_name()
    {
        return name;
    }
}

