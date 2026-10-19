#!/usr/bin/env python3
"""Read-only baseline audit. Writes aggregates, never extension/custom payloads or device data."""
from pathlib import Path
import collections, datetime, hashlib, json, re, statistics, sys, math
BASE=Path('/Users/riversidefm/src/client-monitor-js/src')
NAMES=['stats-27b1ec80-6c9b-4ff2-902f-3ebb8e204acc (1).jsonl','stats-fd1603db-d1d2-4c07-98f3-713dff097cb1.jsonl','stats-fdc17746-4fff-4ae7-9aa8-471581a69200.jsonl','stats-691b798a-bb4b-445f-866b-4c9e162168bf.jsonl','stats-172d5307-a934-4507-ba3f-0adf374604e2.jsonl']
EVENTS=set(re.findall(r"^\s*\w+\s*=\s*'([^']+)'",(BASE/'schema/ClientEventTypes.ts').read_text(),re.M))
META=set(re.findall(r"^\s*\w+\s*=\s*'([^']+)'",(BASE/'schema/ClientMetaTypes.ts').read_text(),re.M))
ISSUES=set(re.findall(r"&\s*\{\s*type:\s*'([^']+)'",(BASE/'ClientMonitorIssues.ts').read_text()))
schema=re.sub(r'/\*.*?\*/','',(BASE/'schema/ClientSample.ts').read_text(),flags=re.S)
TYPES={m.group(1):set(re.findall(r'^\s*(\w+)\??:',m.group(2),re.M)) for m in re.finditer(r'export type (\w+) = \{(.*?)\n\}',schema,re.S)}
GROUPS={'inboundRtps':'InboundRtpStats','outboundRtps':'OutboundRtpStats','remoteInboundRtps':'RemoteInboundRtpStats','remoteOutboundRtps':'RemoteOutboundRtpStats','mediaSources':'MediaSourceStats','mediaPlayouts':'MediaPlayoutStats','iceTransports':'IceTransportStats','iceCandidatePairs':'IceCandidatePairStats','iceCandidates':'IceCandidateStats','codecs':'CodecStats','inboundTracks':'InboundTrackSample','outboundTracks':'OutboundTrackSample','dataChannels':'DataChannelStats'}
def distribution(v):
 if not v:return None
 v=sorted(v);return {'n':len(v),'min':v[0],'median':statistics.median(v),'p95':v[min(len(v)-1,math.ceil(.95*len(v))-1)],'max':v[-1]}
def finite(v):return isinstance(v,(int,float)) and not isinstance(v,bool) and abs(v)<float('inf')
def iso(t):return datetime.datetime.fromtimestamp(t/1000,datetime.timezone.utc).isoformat()
result={'scope':'Built-in Client Monitor types and serialized raw stat fields only. All extension stats, all attachments, custom event/metadata types, Observer-detected findings excluded. No mediasoup router or call-summary reports were supplied; those remain eligible structural/lifecycle inputs separately. No custom payload values persisted.','files':[]}
callAliases={}
for index,name in enumerate(NAMES):
 p=Path('/Users/riversidefm/Downloads')/name;rows=[];invalid=0
 for line in p.open():
  if not line.strip():continue
  try:d=json.loads(line)
  except json.JSONDecodeError:invalid+=1;continue
  if isinstance(d,dict) and 'timestamp' in d:rows.append(d)
 if not rows:continue
 ev=collections.Counter();evx=collections.Counter();meta=collections.Counter();metax=collections.Counter();its=collections.Counter();itx=collections.Counter();families=collections.Counter();coverage=collections.Counter();extras=collections.Counter();famsByMedia=collections.Counter();gauges=collections.defaultdict(list);counterTotals=collections.Counter();corrections=collections.Counter();repeat=collections.Counter();missingRefs=collections.Counter();scores=collections.defaultdict(list);reasonNames=collections.Counter();issueRows=[];ext=0;previous={};seenGauges=set();allIds=collections.defaultdict(set);issuePayloadKeys=collections.defaultdict(set);eventFields=collections.defaultdict(set);metaFields=collections.defaultdict(set)
 for lineno,d in enumerate(rows,1):
  ext+=len(d.get('extensionStats',[]) or [])
  if finite(d.get('score')):scores['client'].append(d['score'])
  for group,allow,c,cx in [('clientEvents',EVENTS,ev,evx),('clientMetaItems',META,meta,metax),('clientIssues',ISSUES|{i+'-resolved' for i in ISSUES},its,itx)]:
   for item in d.get(group,[]) or []:
    if not isinstance(item,dict):continue
    typ=item.get('type','?')
    (c if typ in allow else cx)[typ]+=1
    if typ not in allow:continue
    payload=item.get('payload')
    if isinstance(payload,dict):
     target=issuePayloadKeys if group=='clientIssues' else eventFields if group=='clientEvents' else metaFields
     target[typ].update(payload.keys())
    if group=='clientIssues':issueRows.append({'type':typ,'key':item.get('key'),'timestamp':item.get('timestamp'),'payload':payload if isinstance(payload,dict) else {},'line':lineno})
  for pc in d.get('peerConnections',[]) or []:
   pcid=pc.get('peerConnectionId');localids={g:{x.get('id') for x in pc.get(g,[]) or []} for g in GROUPS}
   if finite(pc.get('score')):scores['pc'].append(pc['score'])
   for group,typename in GROUPS.items():
    for raw in pc.get(group,[]) or []:
     if not isinstance(raw,dict):continue
     r={k:v for k,v in raw.items() if k in TYPES[typename] and k!='attachments'}
     families[group]+=1;famsByMedia[group+':'+r.get('kind','n/a')]+=1
     for k,v in r.items():
      if v is not None:coverage[group+'.'+k]+=1
     extras.update(group+'.'+k for k in raw if k not in TYPES[typename])
     if group.endswith('Tracks') and finite(r.get('score')):scores[group].append(r['score'])
     for reason in (r.get('scoreReasons') or {}):reasonNames[reason]+=1
     ident=(pcid,group,r.get('id'));ts=r.get('timestamp');allIds[group].add(ident)
     if not finite(ts):continue
     prev=previous.get(ident);previous[ident]=r
     if prev and ts==prev.get('timestamp'):repeat[group]+=1
     if prev and finite(prev.get('timestamp')) and ts>prev['timestamp']:
      dt=(ts-prev['timestamp'])/1000
      for field in ['freezeCount','totalFreezesDuration','pauseCount','totalPausesDuration','framesDropped','concealedSamples','silentConcealedSamples','concealmentEvents','synthesizedSamplesDuration','synthesizedSamplesEvents','totalSamplesDuration','bytesSent','bytesReceived','packetsLost','packetsReceived','framesEncoded','framesDecoded','framesRendered','totalDecodeTime','totalEncodeTime']:
       if finite(r.get(field)) and finite(prev.get(field)):
        delta=r[field]-prev[field]
        if delta<0:corrections[group+'.'+field]+=1
        else:counterTotals[group+'.'+field]+=delta
      if group in ['inboundRtps','remoteInboundRtps']:
       lost=r.get('packetsLost');pr=r.get('packetsReceived');pl=prev.get('packetsLost');pp=prev.get('packetsReceived')
       if all(finite(x) for x in [lost,pr,pl,pp]) and lost>=pl and pr>=pp and lost-pl+pr-pp>0:gauges[group+'.lossFraction'].append((lost-pl)/(lost-pl+pr-pp))
      if group=='inboundRtps' and r.get('kind')=='audio':
       vals=[r.get(k) for k in ['concealedSamples','silentConcealedSamples','totalSamplesReceived']]+[prev.get(k) for k in ['concealedSamples','silentConcealedSamples','totalSamplesReceived']]
       if all(finite(x) for x in vals):
        c,s,t,prior_c,ps,pt=vals
        if t>pt and c>=prior_c and s>=ps:gauges['audio.nonSilentConcealmentFraction'].append(max(0,c-prior_c-s+ps)/(t-pt))
      if group=='inboundRtps' and finite(r.get('totalFreezesDuration')) and finite(prev.get('totalFreezesDuration')):
       delta=r['totalFreezesDuration']-prev['totalFreezesDuration']
       if delta>dt:corrections['freezeDurationExceedsReportInterval']+=1
     if ident+(ts,) in seenGauges:continue
     seenGauges.add(ident+(ts,))
     for f in ['jitter','currentRoundTripTime','roundTripTime','fractionLost','framesPerSecond','frameWidth','frameHeight','score']:
      if finite(r.get(f)):gauges[group+'.'+f].append(r[f])
     if group in ['inboundRtps','outboundRtps']:
      for ref,g in [('codecId','codecs'),('transportId','iceTransports'),('mediaSourceId','mediaSources'),('playoutId','mediaPlayouts')]:
       if r.get(ref) and r[ref] not in localids[g]:missingRefs[group+'.'+ref]+=1
 # Pair lifecycle by key and optional raisedAt, preserving unresolved/orphans.
 active={};episodes=[];orphans=0;unkeyed=0
 for i in sorted(issueRows,key=lambda x:(x['timestamp'] if finite(x['timestamp']) else rows[x['line']-1]['timestamp'],x['line'])):
  if i['type'].endswith('-resolved'):
   prev=active.pop(i['key'],None) if i['key'] else None
   if prev:
    duration=i['timestamp']-prev['timestamp'] if finite(i['timestamp']) and finite(prev['timestamp']) else None
    comment=i['payload'].get('comment');end='recovered' if isinstance(comment,str) and ('recover' in comment or 'keeping up' in comment or 'ended' in comment and 'track ended' not in comment) else 'other-or-unknown'
    episodes.append({'type':prev['type'],'closed':True,'durationMs':duration,'ending':end,'raiseLine':prev['line'],'resolveLine':i['line']})
   else:orphans+=1
  elif i['key']:
   if i['key'] in active:corrections['duplicateActiveIssueKey']+=1
   active[i['key']]=i
  else:unkeyed+=1;episodes.append({'type':i['type'],'closed':False,'durationMs':None,'ending':'unkeyed','raiseLine':i['line']})
 episodes += [{'type':i['type'],'closed':False,'durationMs':None,'ending':'right-censored','raiseLine':i['line']} for i in active.values()]
 episodeSummary={}
 for typ in sorted({x['type'] for x in episodes}):
  es=[x for x in episodes if x['type']==typ];episodeSummary[typ]={'raised':len(es),'closed':sum(x['closed'] for x in es),'notClosed':sum(not x['closed'] for x in es),'closedDurationMs':distribution([x['durationMs'] for x in es if x['durationMs'] is not None])}
 times=[r['timestamp'] for r in rows];call=rows[0].get('callId');callAliases.setdefault(call,'Call '+str(len(callAliases)+1));intervals=[b-a for a,b in zip(times,times[1:])]
 rec={'alias':chr(65+index),'file':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'records':len(rows),'invalidJson':invalid,'callAlias':callAliases[call],'distinctClientIds':len({r.get('clientId') for r in rows}),'distinctCallIds':len({r.get('callId') for r in rows}),'startAt':times[0],'endAt':times[-1],'startUtc':iso(times[0]),'endUtc':iso(times[-1]),'spanMs':max(times)-min(times),'sampleIntervalMs':distribution(intervals),'nonIncreasingSampleIntervals':sum(t<=0 for t in intervals),'extensionsExcluded':ext,'eventsAllowed':dict(ev),'eventsExcluded':dict(evx),'metadataAllowed':dict(meta),'metadataExcluded':dict(metax),'issuesAllowed':dict(its),'issuesExcluded':dict(itx),'issueEpisodes':episodeSummary,'orphanResolutions':orphans,'unkeyedRaises':unkeyed,'families':dict(families),'distinctStatIdentities':{k:len(v) for k,v in allIds.items()},'familyMediaRecords':dict(famsByMedia),'fieldPresence':dict(coverage),'unknownRawFieldsExcluded':dict(extras),'counterDeltaTotals':dict(counterTotals),'counterCorrectionsAndAnomalies':dict(corrections),'repeatedStatTimestamps':dict(repeat),'sameSnapshotMissingReferences':dict(missingRefs),'metricDistributions':{k:distribution(v) for k,v in gauges.items()},'scores':{k:distribution(v) for k,v in scores.items()},'scoreReasonTypes':dict(reasonNames),'issuePayloadFieldNames':{k:sorted(v) for k,v in issuePayloadKeys.items()},'eventPayloadFieldNames':{k:sorted(v) for k,v in eventFields.items()},'metadataPayloadFieldNames':{k:sorted(v) for k,v in metaFields.items()}}
 result['files'].append(rec)
 print(json.dumps({k:rec[k] for k in ['alias','records','callAlias','startUtc','spanMs','sampleIntervalMs','extensionsExcluded','issueEpisodes','orphanResolutions','unkeyedRaises','counterCorrectionsAndAnomalies','sameSnapshotMissingReferences','scores']}))
out=Path(__file__).with_name('supplied-samples-baseline-audit.json');out.write_text(json.dumps(result,indent=2)+'\n')
