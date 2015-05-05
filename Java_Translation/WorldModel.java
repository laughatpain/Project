import org.junit.Test;

import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class WorldModel
{
    protected int num_rows;
    protected int num_cols;
    protected Grid background;
    protected Grid occupancy;
    protected ArrayList<Entity> entities;
    protected OrderedList action_queue;

    public WorldModel (int num_rows, int num_cols, WorldObject background)
    {
        this.num_rows = num_rows;
        this.num_cols = num_cols;
        this.background = new Grid(num_cols, num_rows, background);
        this.occupancy = new Grid(num_cols, num_rows, null);
        OrderedList ordered_list = new OrderedList();
        this.action_queue = ordered_list;
        this.entities = new ArrayList<Entity>();

    }
    public boolean within_bounds (Point pt)
    {
        return ((pt.xCoor() >= 0) && (pt.xCoor() < num_cols) && (pt.yCoor() >= 0) &&
                (pt.yCoor() < num_rows));
    }
    public boolean is_occupied (Point pt)
    {
        return (within_bounds(pt) &&
                occupancy.get_cell(pt) != null);
    }
    public WorldObject nearest_entity (ArrayList<Entity> entities, ArrayList<Double> distance)
    {
        if (entities.size() == 0)
        {
            return null;
        }
        double pair = distance.get(0);
        int idx = 0;
        for (int i = 0; i < entities.size(); i++)
        {
            if (distance.get(i) < pair)
            {
                pair = distance.get (i);
                idx = i;
            }
        }
        return entities.get(idx);
    }

    public WorldObject find_nearest (Point pt, Entity type)
    {
        ArrayList<Entity> oftype = new ArrayList<Entity>();
        ArrayList<Double> distance = new ArrayList<Double>();
        WorldObject nearest = entities.get(0);
        for (Entity ent : entities)
        {
            if (ent instanceof Entity)
            {
                oftype.add(ent);
                distance.add(distance_sq(pt, ent.get_position()));
            }
        }
        return nearest_entity(oftype, distance);
    }
    public void add_entity(Entity entity)
    {
        Point pt = entity.get_position();
        if (within_bounds(pt));
        {
            Entity old_entity = (Entity) occupancy.get_cell(pt);
            if (old_entity != null)
            {
                old_entity.get_pending_actions();
            }
            occupancy.set_cell(pt, entity);
            entities.add(entity);
        }
    }
    public ArrayList<Point> move_entity (Entity entity, Point pt)
    {
        ArrayList<Point> tiles= new ArrayList<Point>();
        if (within_bounds(pt));
        {
            Point old_pt = entity.get_position ();
            occupancy.set_cell(old_pt, null);
            tiles.add(old_pt);
            occupancy.set_cell (pt, entity);
            tiles.add(pt);
            entity.set_position(pt);
        }
        return tiles;
    }
    public void remove_entity (Entity entity)
    {
        remove_entity_at(entity.get_position());
    }
    public void remove_entity_at (Point pt)
    {
        if ((within_bounds(pt) && (occupancy.get_cell(pt)) != null))
        {
            Entity entity = (Entity) occupancy.get_cell(pt);
            entity.set_position(new Point(-1, -1));
            entities.remove(entity);
            occupancy.set_cell(pt, null);
        }
    }
    public WorldObject get_background (Point pt)
    {
        if  (within_bounds(pt))
        {
            return background.get_cell(pt);
        }
        else
        {
            return null;
        }
    }
    public void set_background (Point pt, WorldObject bgnd)
    {
        if (within_bounds(pt))
        {
          background.set_cell(pt, bgnd);
        }
    }
    public WorldObject get_tile_occupant (Point pt)
    {
        return occupancy.get_cell(pt);
    }


    public ArrayList<Entity> get_entities()
    {
        return entities;
    }
    public double distance_sq (Point p1, Point p2)
    {
        return ((p1.xCoor() - p2.xCoor()*(p1.xCoor() - p2.xCoor())) +
                ((p1.yCoor() - p2.yCoor())*(p1.yCoor() - p2.yCoor())));
    }
}
