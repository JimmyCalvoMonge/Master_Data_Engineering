import com.ntic.classes.planner.Train
import com.ntic.classes.planner.Time

val TrainObj = new Train("Hello", 12)

val TimeObj = new Time(4, 23)
println(TimeObj.asMinutes)
val TimeObj2 = new Time(4, 15)
println(TimeObj2.asMinutes)

var diff: Int = TimeObj.minus(TimeObj2)
println(diff)

var diff2: Int = TimeObj - TimeObj2
println(diff2)

val TimeObj3 = new Time()
println(TimeObj3.asMinutes)