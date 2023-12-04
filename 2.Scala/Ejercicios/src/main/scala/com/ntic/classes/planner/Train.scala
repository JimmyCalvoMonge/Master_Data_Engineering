package com.ntic.classes.planner
case class Train(info: TrainInfo, schedule: Seq[(Time, Station)]) {
  require(schedule.size >= 2, "schedule debe tener al menos dos elementos")
  val stations: Seq[Station] =
    schedule.map(stop => stop._2)
  def timeAt(station: Station): Option[Time] = {
    // stations.find(s => s == station)
    schedule.find(stop => stop._2 == station).map(found => found._1)
  }
}
case class Station(name: String)
sealed abstract class TrainInfo {
  def number: Int
}
case class InterCityExpress(number: Int, hasWifi: Boolean = false) extends TrainInfo
case class RegionalExpress(number: Int) extends TrainInfo
case class BavarianRegional(number: Int) extends TrainInfo