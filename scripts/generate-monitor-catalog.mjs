// Generate public field/accessor declarations, including constructor parameter properties.
// No schema-membership heuristic is used to guess a field's origin.
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { execFileSync } from 'node:child_process';
import ts from 'typescript';
const input = process.argv[2];
if (!input) throw new Error('Usage: node scripts/generate-monitor-catalog.mjs /path/to/client-monitor-js');
const root = resolve(input);
const expected = '0f08bd5d110a4e9d53cf0486962e638c5b393c49';
const revision = execFileSync('git', ['-C', root, 'rev-parse', 'HEAD'], {encoding:'utf8'}).trim();
if (revision !== expected) throw new Error('Source revision differs from the baseline. Review versions and documentation before regenerating.');
if (execFileSync('git', ['-C', root, 'status', '--porcelain', '--', 'src'], {encoding:'utf8'}).trim()) throw new Error('Source has local edits; use the clean pinned snapshot.');
const files = ['src/ClientMonitor.ts', ...readdirSync(join(root, 'src/monitors')).filter(f => f.endsWith('.ts')).map(f => `src/monitors/${f}`)];
const monitors = [];
const privateMember = node => node.modifiers?.some(m => [ts.SyntaxKind.PrivateKeyword, ts.SyntaxKind.ProtectedKeyword].includes(m.kind));
for (const file of files) {
  const source = ts.createSourceFile(file, readFileSync(join(root,file),'utf8'), ts.ScriptTarget.Latest, true);
  const baseUrl = `https://github.com/ObserveRTC/client-monitor-js/blob/${revision}/${file}`;
  const urlOf = node => `${baseUrl}#L${source.getLineAndCharacterOfPosition(node.getStart(source)).line + 1}`;
  for (const node of source.statements) {
    if (!ts.isClassDeclaration(node)) continue;
    const members = [];
    const add = (member, declaration) => {
      const name = member.name?.getText(source);
      if (!name || name === 'visited' || name.startsWith('#') || privateMember(member)) return;
      members.push({name, declaration, url:urlOf(member)});
    };
    for (const member of node.members) {
      if (ts.isPropertyDeclaration(member) || ts.isGetAccessorDeclaration(member)) add(member, member.getText(source).split('\n')[0]);
      if (ts.isConstructorDeclaration(member)) {
        for (const parameter of member.parameters) {
          if (parameter.modifiers?.some(m => [ts.SyntaxKind.PublicKeyword,ts.SyntaxKind.ReadonlyKeyword].includes(m.kind))) add(parameter, parameter.getText(source));
        }
      }
    }
    monitors.push({name:node.name.text, url:urlOf(node), members});
  }
}
writeFileSync(new URL('../data/monitors.json', import.meta.url), JSON.stringify(monitors,null,2)+'\n');
console.log(`Generated ${monitors.length} monitors and ${monitors.reduce((n,m)=>n+m.members.length,0)} public declarations from ${revision}.`);
