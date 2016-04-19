#!/usr/bin/python

#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import argparse
import pydot
import os

def main(args=None):
    parser = argparse.ArgumentParser(description='Attack Tree to CAIRIS Model converter')
    parser.add_argument('dotFile',help='attack tree model to import (Dot format)')
    parser.add_argument('--context',dest='contextName',help='attack context')
    parser.add_argument('--author',dest='originatorName',help='author/s')
    parser.add_argument('--out',dest='outFile',help='output file (CAIRIS format)')
    args = parser.parse_args()

    xmlBuf = '<?xml version="1.0"?>\n<!DOCTYPE cairis_model PUBLIC "-//CAIRIS//DTD MODEL 1.0//EN" "http://cairis.org/dtd/cairis_model.dtd">\n\n<cairis_model>\n\n'
   
    xmlBuf += '<cairis>\n  <project_settings name="' + args.contextName + '">\n    <contributors>\n      <contributor first_name="None" surname="None" affiliation="' + args.originatorName + '" role="Scribe" />\n    </contributors>\n  </project_settings>\n  <environment name="' + args.contextName + '" short_code="' + args.contextName + '">\n    <definition>' + args.contextName + '</definition>\n    <asset_values>\n      <none>TBC</none>\n      <low>TBC</low>\n      <medium>TBC</medium>\n      <high>TBC</high>\n    </asset_values>\n  </environment>\n</cairis>\n\n'
    dotInstance = pydot.graph_from_dot_file(args.dotFile)

    goals = []
    obstacles = []
    acs = {}

    for node in dotInstance.get_node_list():
      nodeShape = node.get_shape()
      nodeStyle = str(node.get_style())
     
      if nodeShape == 'box' and nodeStyle == 'rounded':
        obstacles.append(node.get_name())
      elif nodeShape == 'box' and nodeStyle == 'None':
        nodeName = node.get_name()
        if (nodeName != 'node' and nodeName != 'edge'):
          goals.append(node.get_name())
      elif nodeShape == 'triangle':
        acs[node.get_name()] = node.get_label()
 
    xmlBuf += '<goals>\n'

    for g in goals:
      xmlBuf += '  <goal name=' + g + ' originator="' + args.originatorName + '">\n    <goal_environment name="' + args.contextName + '" category="Maintain" priority="Medium">\n      <definition>' + g + '</definition>\n      <fit_criterion>TBC</fit_criterion>\n      <issue>None</issue>\n    </goal_environment>\n  </goal>\n'

    for o in obstacles:
      xmlBuf += '  <obstacle name=' + o + ' originator="' + args.originatorName + '">\n    <obstacle_environment name="' + args.contextName + '" category="Threat">\n      <definition>' + g + '</definition>\n    </obstacle_environment>\n  </obstacle>\n'

    xmlBuf += '</goals>\n\n'

    fromAssocs = []
    toAssocs = {}
    assocs = []

    for e in dotInstance.get_edge_list():
      fromName = e.get_source()
      toName = e.get_destination()
      if fromName in acs:
        if fromName not in toAssocs:
          toAssocs[fromName] = [toName]
        else:
          toAssocs[fromName].append(toName)
      elif toName in acs:
        fromAssocs.append((fromName,toName))
      else:
        assocs.append('  <goal_association environment="' + args.contextName + '" goal_name=' + fromName + ' goal_dim="obstacle" ref_type="resolve" subgoal_name=' + toName + ' subgoal_dim="goal" alternative_id="0">\n    <rationale>None</rationale>\n  </goal_association>\n')

    for fromName,toName in fromAssocs:
      for subGoalName in toAssocs[toName]: 
        assocs.append('  <goal_association environment="' + args.contextName + '" goal_name=' + fromName + ' goal_dim="obstacle" ref_type=' + acs[toName] + ' subgoal_name=' + subGoalName + ' subgoal_dim="obstacle" alternative_id="0">\n    <rationale>None</rationale>\n  </goal_association>\n')

    xmlBuf += '<associations>\n'
    for assoc in assocs:
      xmlBuf += assoc    
    xmlBuf += '</associations>\n\n</cairis_model>'

    f = open(args.outFile,'w')
    f.write(xmlBuf)
    f.close()
    print args.outFile + ' created'

if __name__ == '__main__':
  main()
