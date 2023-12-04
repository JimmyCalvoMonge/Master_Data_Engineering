package com.ntic.classes.planner
class JourneyPlanner(trains: Set[Train]) {
  val stations: Set[Station] =
    trains.flatMap(train => train.stations)
  def trainsAt(station: Station): Set[Train] =
    trains.filter(train => train.stations contains station)

  def stopsAt(station: Station): Set[(Time, Train)] =
    for {
      train <- trains
      (time, `station`) <- train.schedule
    } yield (time, train)
  def isShortTrip(from: Station, to: Station): Boolean =
    trains.exists(train =>
      train.stations.dropWhile(station => station != from) match {
        case `from` +: `to` +: _ => true
        case `from` +: _ +: `to` +: _ => true
        case _ => false
      }
    )
}