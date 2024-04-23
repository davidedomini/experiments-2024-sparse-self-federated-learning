package it.unibo.alchemist.model.implementations.reactions

import it.unibo.alchemist.model.{Environment, Position, TimeDistribution}
import it.unibo.alchemist.model.molecules.SimpleMolecule
import it.unibo.scafi.interop.PythonModules.{torch, utils}
import me.shadaj.scalapy.py

import scala.util.Random

class CentralLearnerReaction [T, P <: Position[P]](
    environment: Environment[T, P],
    distribution: TimeDistribution[T],
    seed: Int,
    clientsFraction: Double
) extends AbstractGlobalReaction(environment, distribution){

  override protected def executeBeforeUpdateDistribution(): Unit = {
    val time = environment.getSimulation.getTime.toDouble
    if (time > 1) { // skip the first tick
      val clients = (environment.getNodes.size() * clientsFraction).toInt
      val localModels = getModels(clients)
      val globalModel = averageWeights(localModels)
      nodes.foreach(n => n.setConcentration(new SimpleMolecule("Model"), globalModel.asInstanceOf[T]))
      snapshot(globalModel, time.toInt)
    }
  }
  
  private def getModels(requiredModels: Int): List[py.Dynamic] = {
    val models = nodes
      .map(_.getConcentration(new SimpleMolecule("Model")).asInstanceOf[py.Dynamic])
    new Random(seed).shuffle(models).take(requiredModels)
  }

  private def averageWeights(localModels: Seq[py.Dynamic]): py.Dynamic = {
      utils.average_weights(localModels.toPythonProxy)
  }

  private def snapshot(model: py.Dynamic, time: Double): Unit = {
    torch.save(
      model,
      s"networks-baseline/model-$time"
    )
  }

}
