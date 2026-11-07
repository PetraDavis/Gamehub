// Sends Python files from the browser to a TI-84 Evo over USB.
//
// The Evo transfer details (Kermit packets, the Python container format and
// the hh01/xfr/var upload address) come from TI-84-Evo-tools by Nomadtax,
// https://github.com/The-Real-NomadTax/TI-84-Evo-tools, MIT License,
// Copyright (c) 2026 Nomadtax. This file is a JavaScript port of the parts
// needed to upload a .py file.
(function () {
  'use strict';
  const VENDOR = 0x0451, PRODUCT = 0xe018, PY_TYPE = 15;
  const enc = new TextEncoder(), dec = new TextDecoder();
  const toChar = v => v + 32;
  const fromChar = v => v - 32;

  function checksum1(bytes) {
    let s = 0;
    for (const b of bytes) s = (s + b) & 0xffff;
    return (s + ((s & 0xc0) >> 6)) & 0x3f;
  }

  function packet(seq, kind, data) {
    data = data || [];
    const k = typeof kind === 'string' ? kind.charCodeAt(0) : kind;
    let p;
    if (data.length > 91) {
      const xl = data.length + 1;
      p = [1, toChar(0), toChar(seq & 63), k, toChar(Math.floor(xl / 95)), toChar(xl % 95)];
      p.push(toChar(checksum1(p.slice(1))));
      for (const b of data) p.push(b);
    } else {
      p = [1, toChar(data.length + 3), toChar(seq & 63), k];
      for (const b of data) p.push(b);
    }
    p.push(toChar(checksum1(p.slice(1))));
    p.push(13);
    return new Uint8Array(p);
  }

  // MAXL TIME NPAD PADC EOL QCTL QBIN CHKT REPT CAPAS WINDO MAXLX1 MAXLX2
  const INIT = Array.from(enc.encode('~0 @-#Y1~."5M'));

  function attributes(n) {
    const len = String(n);
    return Array.from(enc.encode('""B81')).concat([toChar(len.length)], Array.from(enc.encode(len)), [64, 32]);
  }

  function chunks(data, max) {
    const out = [];
    let cur = [];
    for (const v of data) {
      const low = v & 0x7f;
      let e;
      if (low < 0x20 || low === 0x7f) e = [35, v ^ 0x40];
      else if (v === 35 || v === 126) e = [35, v];
      else e = [v];
      if (cur.length && cur.length + e.length > max) { out.push(cur); cur = []; }
      for (const b of e) cur.push(b);
    }
    if (cur.length) out.push(cur);
    return out;
  }

  function decodeData(e) {
    const out = [];
    for (let i = 0; i < e.length; i++) {
      let rep = 1;
      if (e[i] === 126) { rep = fromChar(e[i + 1]); i += 2; }
      let v = e[i];
      if (v === 35) {
        i++; v = e[i];
        const low = v & 0x7f;
        if (low === 63 || (low >= 64 && low <= 95)) v ^= 0x40;
      }
      for (let r = 0; r < rep; r++) out.push(v);
    }
    return out;
  }

  // Returns {pkt, used} or null when more bytes are needed.
  function parse(buf) {
    const s = buf.indexOf(1);
    if (s < 0 || buf.length < s + 6) return null;
    const len = fromChar(buf[s + 1]);
    if (len !== 0) {
      const end = s + len + 3;
      if (buf.length < end) return null;
      return { pkt: { seq: fromChar(buf[s + 2]), kind: String.fromCharCode(buf[s + 3]), data: buf.slice(s + 4, end - 2) }, used: end };
    }
    if (buf.length < s + 9) return null;
    const xl = fromChar(buf[s + 4]) * 95 + fromChar(buf[s + 5]);
    const end = s + 7 + xl + 1;
    if (buf.length < end) return null;
    return { pkt: { seq: fromChar(buf[s + 2]), kind: String.fromCharCode(buf[s + 3]), data: buf.slice(s + 7, end - 2) }, used: end };
  }

  // ---- Python container (CBOR) ----
  function cborHead(out, major, v) {
    const p = major << 5;
    if (v < 24) out.push(p | v);
    else if (v < 0x100) out.push(p | 24, v);
    else if (v < 0x10000) out.push(p | 25, v >> 8, v & 255);
    else out.push(p | 26, (v >>> 24) & 255, (v >> 16) & 255, (v >> 8) & 255, v & 255);
  }
  function cborText(out, s) { const b = enc.encode(s); cborHead(out, 3, b.length); for (const x of b) out.push(x); }
  function cborBytes(out, b) { cborHead(out, 2, b.length); for (const x of b) out.push(x); }
  function u32(out, v) { out.push(v & 255, (v >> 8) & 255, (v >> 16) & 255, (v >>> 24) & 255); }

  function pythonContainer(name, src) {
    const prog = [];
    u32(prog, 0x113);
    u32(prog, src.length + name.length + 18);
    u32(prog, name.length);
    for (const c of enc.encode(name)) prog.push(c);
    prog.push(0, src.length & 255, (src.length >> 8) & 255, (src.length >> 16) & 255, 2);
    for (const c of src) prog.push(c);
    prog.push(0);
    const tok = [];
    for (const c of enc.encode(name)) tok.push(c - 65, 0xe8);
    const out = [0xbf];
    cborText(out, 'metaData'); out.push(0xbf);
    cborText(out, 'type'); cborHead(out, 0, PY_TYPE);
    cborText(out, 'version'); cborHead(out, 0, 1);
    cborText(out, 'name'); cborBytes(out, tok);
    out.push(0xff);
    cborText(out, 'version'); cborHead(out, 0, 1);
    cborText(out, 'size'); cborHead(out, 0, prog.length);
    cborText(out, 'data'); cborBytes(out, prog);
    out.push(0xff);
    return out;
  }

  function wireName(name) {
    let s = '';
    for (const c of name) s += String.fromCharCode(0xe800 + c.charCodeAt(0) - 65);
    return encodeURIComponent(s);
  }

  // ---- transports ----
  async function openSerial() {
    const port = await navigator.serial.requestPort({ filters: [{ usbVendorId: VENDOR, usbProductId: PRODUCT }] });
    await port.open({ baudRate: 115200 });
    const writer = port.writable.getWriter();
    const reader = port.readable.getReader();
    let pending = null;
    return {
      kind: 'serial',
      write: d => writer.write(d),
      read: async ms => {
        if (!pending) pending = reader.read();
        const r = await Promise.race([pending, new Promise(res => setTimeout(() => res('timeout'), ms))]);
        if (r === 'timeout') return null;
        pending = null;
        return r.value || new Uint8Array(0);
      },
      close: async () => { try { reader.cancel(); } catch (e) {} try { reader.releaseLock(); writer.releaseLock(); } catch (e) {} try { await port.close(); } catch (e) {} },
    };
  }

  async function openUsb() {
    const dev = await navigator.usb.requestDevice({ filters: [{ vendorId: VENDOR, productId: PRODUCT }] });
    await dev.open();
    if (dev.configuration === null) await dev.selectConfiguration(1);
    let found = null;
    for (const itf of dev.configuration.interfaces) {
      for (const alt of itf.alternates) {
        let i = null, o = null;
        for (const ep of alt.endpoints) {
          if (ep.type !== 'bulk') continue;
          if (ep.direction === 'in') i = ep.endpointNumber; else o = ep.endpointNumber;
        }
        if (i !== null && o !== null) { found = { n: itf.interfaceNumber, i, o }; break; }
      }
      if (found) break;
    }
    if (!found) throw new Error('No data connection found on the calculator.');
    await dev.claimInterface(found.n);
    let pending = null;
    return {
      kind: 'usb',
      write: d => dev.transferOut(found.o, d),
      read: async ms => {
        if (!pending) pending = dev.transferIn(found.i, 512);
        const r = await Promise.race([pending, new Promise(res => setTimeout(() => res('timeout'), ms))]);
        if (r === 'timeout') return null;
        pending = null;
        return new Uint8Array(r.data.buffer, r.data.byteOffset, r.data.byteLength);
      },
      close: async () => { try { await dev.releaseInterface(found.n); await dev.close(); } catch (e) {} },
    };
  }

  // ---- upload session ----
  async function session(link, dest, contents) {
    let buf = [];
    async function ack(seq, what) {
      const t0 = Date.now();
      while (Date.now() - t0 < 8000) {
        let p = parse(buf);
        while (!p) {
          const chunk = await link.read(2000);
          if (chunk === null) { if (Date.now() - t0 > 8000) break; continue; }
          for (const b of chunk) buf.push(b);
          p = parse(buf);
          if (Date.now() - t0 > 8000) break;
        }
        if (!p) break;
        buf = buf.slice(p.used);
        const k = p.pkt.kind;
        if (k === 'Y' && p.pkt.seq === (seq & 63)) return;
        if (k === 'N') throw new Error('The calculator said no while ' + what + '.');
        if (k === 'E') throw new Error('The calculator said: ' + dec.decode(new Uint8Array(decodeData(p.pkt.data))));
      }
      throw new Error('No answer from the calculator while ' + what + '.');
    }
    await link.write(packet(0, 'S', INIT)); await ack(0, 'starting');
    await link.write(packet(1, 'F', Array.from(enc.encode(dest)))); await ack(1, 'opening the file');
    await link.write(packet(2, 'A', attributes(contents.length))); await ack(2, 'sending the file size');
    let seq = 3;
    for (const c of chunks(contents, 90)) {
      await link.write(packet(seq, 'D', c)); await ack(seq, 'sending data');
      seq = (seq + 1) & 63;
    }
    await link.write(packet(seq, 'Z', [])); await ack(seq, 'saving the file');
    seq = (seq + 1) & 63;
    await link.write(packet(seq, 'B', [])); await ack(seq, 'finishing');
  }

  async function connect(prefer) {
    if (prefer !== 'usb' && 'serial' in navigator) return openSerial();
    if ('usb' in navigator) return openUsb();
    if ('serial' in navigator) return openSerial();
    throw new Error('This browser cannot talk to USB devices. Use Chrome or Edge on a computer.');
  }

  // files: [{name, url}]. onStep(index, state, message)
  async function sendFiles(files, onStep, prefer) {
    const link = await connect(prefer);
    try {
      for (let i = 0; i < files.length; i++) {
        const f = files[i];
        onStep(i, 'busy');
        const res = await fetch(f.url, { cache: 'no-store' });
        if (!res.ok) throw new Error('Could not load ' + f.name + '.py from this site.');
        const src = new Uint8Array(await res.arrayBuffer());
        const body = pythonContainer(f.name, src);
        const dest = 'hh01/xfr/var?name=' + wireName(f.name) + '&type=' + PY_TYPE + '&memtarget=0&policy=0';
        await session(link, dest, body);
        onStep(i, 'done');
        await new Promise(r => setTimeout(r, 250));
      }
    } finally {
      await link.close();
    }
  }

  window.EvoSend = { sendFiles, supported: () => ('serial' in navigator) || ('usb' in navigator), _test: { packet, attributes, chunks, pythonContainer, wireName, parse, decodeData, INIT } };
})();
