package com.ntic.classes.planner
import scala.util.Try
object Time {
  def fromMinutes(minutes: Int): Time =
    Time(minutes / 60, minutes % 60)
  def fromMap(m: Map[String, String]): Option[Time] = {
    // Option 1
    // val hours = Try(m("hours").toInt)
    // val t: String = hours.map(h => Try(m("minutes").toInt).map(m => com.ntic.clases.journeyplanner.Time(h, m)))
    // val t: String = hours.flatMap(h => Try(m("minutes").toInt).map(m => com.ntic.clases.journeyplanner.Time(h, m)))
    // Option 2
    //    for {
    //      hours <- Try(m("hours").toInt)
    //      minutes <- Try(m("minutes").toInt) match {
    //        case Success(value) => Success(value)
    //        case Failure(_) => Success(0)
    //      }
    //    } yield com.ntic.clases.scalaTrain.Time(hours, minutes)
    // Option 3
    val tryTime = for {
      hours <- Try(m("hours").toInt)
      minutes <- Try(m("minutes").toInt).recover({ case _: Exception => 0 })
    } yield Time(hours, minutes)
    tryTime.toOption
  }
}
case class Time(hours: Int = 0, minutes: Int = 0) extends Ordered[Time] {
  require(hours >= 0 && hours <= 23, "hours debe estar entre 0 y 23")
  require(minutes >= 0 && minutes <= 59, "minutes debe estar entre 0 y 59")
  val asMinutes: Int =
    hours * 60 + minutes
  override lazy val toString: String =
    f"$hours%02d:$minutes%02d"
  def minus(that: Time): Int =
    this.asMinutes - that.asMinutes
  def -(that: Time): Int =
    minus(that)
  def toMap: Map[String, String] =
    Map("hours" -> s"$hours", "minutes" -> s"$minutes")
  override def compare(that: Time): Int =
    this - that
}