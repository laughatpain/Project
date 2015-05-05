/**
 * Created by James on 5/4/2015.
 */

import jdk.management.resource.NotifyingMeter;
import org.junit.Test;
import org.junit.Before;

import java.util.ArrayList;

import static org.junit.Assert.*;

public class TestCases
{
    private static final double DELTA = .00001;
    private int i = 1;
    private Point p1 = new Point (1, 2);
    private Point p2 = new Point (2, 3);
    private Point p3 = new Point (-1,-1);
    private Background b1 = new Background("Funk");
    private Entity e1 = new Entity("Yugioh", p1);
    private Moving m1 = new Moving("Slow", p1, 5);
    private NotAnimated na1 = new NotAnimated("Stuck", p1, 3);
    private Miner m2 = new Miner ("FMA", p1, 5, 3, 2);
    private Vein v1 = new Vein ("Earth", p1, 3, 2);
    private WorldModel wm1 = new WorldModel(10, 10, b1);
    private WorldModel wm2 = new WorldModel(10, 10, e1);

    //entities test
    @Test
    public void testXCoor()
    {
        assertEquals(1.0, p1.xCoor(), DELTA);
    }
    @Test
    public void testYCoor()
    {
        assertEquals(2.0, p1.yCoor(), DELTA);
    }
    @Test
    public void testGetName()
    {
        assertEquals(b1.get_name(), "Funk");
    }
    @Test
    public void testGetPosition()
    {
        assertEquals(e1.get_position(), p1);
    }
    @Test
    public void testSetPosition()
    {
        assertEquals(e1.set_position(p2),p2);
    }
    @Test
    public void testGetAnimationRate()
    {
        assertEquals(m1.get_animation_rate(),5);
    }
    @Test
    public void testGetRate ()
    {
        assertEquals(na1.get_rate(), 3);
    }
    @Test
    public void testGetResourceCount ()
    {
        assertEquals(m2.get_resource_count(), 0);
    }
    @Test
    public void testGetResourceLimit ()
    {
        assertEquals(m2.get_resource_limit(), 2);
    }
    @Test
    public void testSetResourceLimit ()
    {
        m2.set_resource_count(2);
        assertEquals(m2.get_resource_count(), 2);
    }
    @Test
    public void testGetResourceDistance ()
    {
        assertEquals(v1.get_resource_distance(), 2);
    }
    //world model tests
    @Test
    public void testWithinBounds ()
    {
        assertTrue(wm1.within_bounds(p1));
    }
    @Test
    public void testWithinBounds2 ()
    {
        assertFalse(wm1.within_bounds(p3));
    }
    @Test
    public void testIsOccupied()
    {
        assertEquals(false, wm1.is_occupied(p1));
    }
    @Test
    public void testAddEntity()
    {
        wm1.add_entity(m2);
        assertTrue(wm1.is_occupied(p1));

        wm1.add_entity(m2);
        assertFalse(wm1.is_occupied(p2));
    }
    @Test
    public void testMoveEntity()
    {
        assertFalse(wm1.is_occupied(p2));

        wm1.move_entity(v1, p2);

        assertTrue(wm1.is_occupied(p2));
    }
    @Test
    public void testRemoveEntity()
    {
        wm1.add_entity(m2);
        wm1.move_entity(m2, p2);
        assertTrue(wm1.is_occupied(p2));
        wm1.remove_entity(m2);
        assertFalse(wm1.is_occupied(p2));
    }
    @Test
    public void testRemoveEntityAt()
    {
        wm1.add_entity(v1);
        assertTrue(wm1.is_occupied(p1));
        wm1.remove_entity_at(p1);
        assertFalse(wm1.is_occupied(p1));
    }
    @Test
    public void testDistanceSq ()
    {
        assertEquals (wm1.distance_sq (p2, p1), 2, DELTA);
    }
    /*
    @Test
    public void testGetBackground ()
    {
    }

    @Test
    public void testSetBackground ()
    {
    }

    @Test
    public void testGetEntities ()
    {
        ArrayList<Entity> l1 = new ArrayList<Entity>();
        l1.add(m2);
        wm1.add_entity(m2);
        assertTrue(wm1.get_entities(), m2);
    }
    @Test
    public void testFindNearest ()
    {
        ArrayList<Entity> l1 = new ArrayList<Entity>();
        wm1.add_entity(m2);
        wm1.add_entity(v1);
        assertTrue(wm1.find_nearest(p1,Miner), m1);
    }
    @Test
    public void testNearestEntity ()
    {
        ArrayList<Entity> l1 = new ArrayList<Entity>();
        ArrayList<Double> l2 = new ArrayList<Double>();
        l1.add(m2);
        l1.add(v1);
        ll.add(v2);
        l1.add(v3);
        l2.wm1.distance_sq(m2, v1);
        l2.wm1.distance_sq(m2, v2);
        l2.wm1.distance_sq(m2, v3);
        assertTrue(wm1.nearest_entity (l1, l2), v3);
    }*/
}
