#set page(
  paper: "a4",
  margin: (top: 2cm, bottom: 2cm, left: 1.5cm, right: 1.5cm),
  header: context {
    if counter(page).get().first() > 1 [
      #align(center)[#text(size: 8pt, fill: luma(120))[Smallest Connected Polyiamond Containing All Fixed n-Iamonds]]
    ]
  },
  footer: context {
    let current = counter(page).get().first()
    let total = counter(page).final().first()
    align(center)[#text(size: 8pt, fill: luma(120))[Page #current of #total]]
  },
)
#set text(font: "New Computer Modern", size: 9pt)

#align(center)[
  #text(size: 16pt, weight: "bold")[Smallest Connected Polyiamond Containing All Fixed n-Iamonds]
  #v(0.3em)
  #text(size: 10pt)[$a(n)$ = minimum number of triangular cells in a connected polyiamond container that contains every fixed $n$-iamond as a translated subset. Rotations and reflections are distinct. Each value is verified inside the strictly wider $(n + 1) times (n + 1)$ search window with a drat-trim VERIFIED DRAT proof of UNSAT at size $a(n) - 1$.]
  #v(0.2em)
  #text(size: 10pt)[$a(1..9) = 2, 4, 6, 9, 12, 17, 22, 27, 31$]
  #v(0.2em)
  #text(size: 8pt, style: "italic")[Computed by Peter Exley, April 2026]
]
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)
#v(0.3em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(1) = 2$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[2 cells, 2 fixed $n$-iamonds, bbox 1 x 2, solved in 0.0s within the search rectangle]
]
#v(0.2em)
#align(center)[
#box(width: 1.70cm, height: 1.07cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.1000cm, 0.1000cm), (1.1000cm, 0.1000cm), (0.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.1000cm), (0.6000cm, 0.9660cm), (1.6000cm, 0.9660cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(2) = 4$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[4 cells, 3 fixed $n$-iamonds, bbox 2 x 2, solved in 0.0s within the search rectangle]
]
#v(0.2em)
#align(center)[
#box(width: 1.70cm, height: 1.93cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.1000cm, 0.1000cm), (1.1000cm, 0.1000cm), (0.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.1000cm), (0.6000cm, 0.9660cm), (1.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 0.9660cm), (0.1000cm, 1.8321cm), (1.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 0.9660cm), (1.6000cm, 0.9660cm), (1.1000cm, 1.8321cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(3) = 6$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[6 cells, 6 fixed $n$-iamonds, bbox 2 x 4, solved in 0.0s within the search rectangle]
]
#v(0.2em)
#align(center)[
#box(width: 2.20cm, height: 1.93cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 0.1000cm), (0.1000cm, 0.9660cm), (1.1000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 0.1000cm), (1.6000cm, 0.1000cm), (1.1000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 0.1000cm), (1.1000cm, 0.9660cm), (2.1000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.1000cm, 0.9660cm), (1.1000cm, 0.9660cm), (0.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.9660cm), (0.6000cm, 1.8321cm), (1.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.9660cm), (2.1000cm, 0.9660cm), (1.6000cm, 1.8321cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(4) = 9$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[9 cells, 14 fixed $n$-iamonds, bbox 3 x 4, solved in 0.0s within the search rectangle]
]
#v(0.2em)
#align(center)[
#box(width: 2.70cm, height: 2.80cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.1000cm, 0.1000cm), (1.1000cm, 0.1000cm), (0.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.1000cm), (0.6000cm, 0.9660cm), (1.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.1000cm), (2.1000cm, 0.1000cm), (1.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 0.1000cm), (1.6000cm, 0.9660cm), (2.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 0.9660cm), (0.1000cm, 1.8321cm), (1.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 0.9660cm), (1.6000cm, 0.9660cm), (1.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 0.9660cm), (1.1000cm, 1.8321cm), (2.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 0.9660cm), (2.6000cm, 0.9660cm), (2.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 1.8321cm), (2.1000cm, 1.8321cm), (1.6000cm, 2.6981cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(5) = 12$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[12 cells, 36 fixed $n$-iamonds, bbox 4 x 6, solved in 0.0s within the search rectangle]
]
#v(0.2em)
#align(center)[
#box(width: 3.20cm, height: 3.66cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 0.1000cm), (1.1000cm, 0.9660cm), (2.1000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.1000cm, 0.9660cm), (1.1000cm, 0.9660cm), (0.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.9660cm), (0.6000cm, 1.8321cm), (1.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.9660cm), (2.1000cm, 0.9660cm), (1.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 0.9660cm), (1.6000cm, 1.8321cm), (2.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 0.9660cm), (3.1000cm, 0.9660cm), (2.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 1.8321cm), (0.1000cm, 2.6981cm), (1.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 1.8321cm), (1.6000cm, 1.8321cm), (1.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 1.8321cm), (1.1000cm, 2.6981cm), (2.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 1.8321cm), (2.6000cm, 1.8321cm), (2.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 1.8321cm), (2.1000cm, 2.6981cm), (3.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 2.6981cm), (2.1000cm, 2.6981cm), (1.6000cm, 3.5641cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(6) = 17$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[17 cells, 94 fixed $n$-iamonds, bbox 4 x 6, solved in 0.0s within the search rectangle]
]
#v(0.2em)
#align(center)[
#box(width: 3.70cm, height: 3.66cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 0.1000cm), (1.6000cm, 0.9660cm), (2.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 0.9660cm), (1.6000cm, 0.9660cm), (1.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 0.9660cm), (1.1000cm, 1.8321cm), (2.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 0.9660cm), (2.6000cm, 0.9660cm), (2.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 0.9660cm), (2.1000cm, 1.8321cm), (3.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.1000cm, 1.8321cm), (1.1000cm, 1.8321cm), (0.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 1.8321cm), (0.6000cm, 2.6981cm), (1.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 1.8321cm), (2.1000cm, 1.8321cm), (1.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 1.8321cm), (1.6000cm, 2.6981cm), (2.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 1.8321cm), (3.1000cm, 1.8321cm), (2.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.1000cm, 1.8321cm), (2.6000cm, 2.6981cm), (3.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 2.6981cm), (0.1000cm, 3.5641cm), (1.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 2.6981cm), (1.6000cm, 2.6981cm), (1.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 2.6981cm), (1.1000cm, 3.5641cm), (2.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 2.6981cm), (2.6000cm, 2.6981cm), (2.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 2.6981cm), (2.1000cm, 3.5641cm), (3.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 2.6981cm), (3.6000cm, 2.6981cm), (3.1000cm, 3.5641cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(7) = 22$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[22 cells, 250 fixed $n$-iamonds, bbox 4 x 7, solved in 0.1s within the search rectangle]
]
#v(0.2em)
#align(center)[
#box(width: 4.20cm, height: 3.66cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.1000cm), (2.1000cm, 0.1000cm), (1.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 0.1000cm), (1.6000cm, 0.9660cm), (2.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 0.1000cm), (3.1000cm, 0.1000cm), (2.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 0.9660cm), (1.6000cm, 0.9660cm), (1.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 0.9660cm), (1.1000cm, 1.8321cm), (2.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 0.9660cm), (2.6000cm, 0.9660cm), (2.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 0.9660cm), (2.1000cm, 1.8321cm), (3.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 0.9660cm), (3.6000cm, 0.9660cm), (3.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.1000cm, 1.8321cm), (1.1000cm, 1.8321cm), (0.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 1.8321cm), (0.6000cm, 2.6981cm), (1.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 1.8321cm), (2.1000cm, 1.8321cm), (1.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 1.8321cm), (1.6000cm, 2.6981cm), (2.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 1.8321cm), (3.1000cm, 1.8321cm), (2.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.1000cm, 1.8321cm), (2.6000cm, 2.6981cm), (3.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.1000cm, 1.8321cm), (4.1000cm, 1.8321cm), (3.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 2.6981cm), (0.1000cm, 3.5641cm), (1.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 2.6981cm), (1.6000cm, 2.6981cm), (1.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 2.6981cm), (1.1000cm, 3.5641cm), (2.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 2.6981cm), (2.6000cm, 2.6981cm), (2.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 2.6981cm), (2.1000cm, 3.5641cm), (3.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 2.6981cm), (3.6000cm, 2.6981cm), (3.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.6000cm, 2.6981cm), (3.1000cm, 3.5641cm), (4.1000cm, 3.5641cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(8) = 27$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[27 cells, 675 fixed $n$-iamonds, bbox 5 x 8, solved in 0.8s within the search rectangle]
]
#v(0.2em)
#align(center)[
#box(width: 4.70cm, height: 4.53cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.1000cm, 0.1000cm), (1.1000cm, 0.1000cm), (0.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.1000cm), (0.6000cm, 0.9660cm), (1.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.1000cm), (2.1000cm, 0.1000cm), (1.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 0.1000cm), (1.6000cm, 0.9660cm), (2.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 0.1000cm), (3.1000cm, 0.1000cm), (2.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.1000cm, 0.1000cm), (2.6000cm, 0.9660cm), (3.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.1000cm, 0.1000cm), (4.1000cm, 0.1000cm), (3.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (4.1000cm, 0.1000cm), (3.6000cm, 0.9660cm), (4.6000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 0.9660cm), (0.1000cm, 1.8321cm), (1.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 0.9660cm), (1.6000cm, 0.9660cm), (1.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 0.9660cm), (1.1000cm, 1.8321cm), (2.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 0.9660cm), (2.6000cm, 0.9660cm), (2.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 0.9660cm), (2.1000cm, 1.8321cm), (3.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 0.9660cm), (3.6000cm, 0.9660cm), (3.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.6000cm, 0.9660cm), (3.1000cm, 1.8321cm), (4.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.6000cm, 0.9660cm), (4.6000cm, 0.9660cm), (4.1000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 1.8321cm), (0.6000cm, 2.6981cm), (1.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 1.8321cm), (2.1000cm, 1.8321cm), (1.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 1.8321cm), (1.6000cm, 2.6981cm), (2.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 1.8321cm), (3.1000cm, 1.8321cm), (2.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.1000cm, 1.8321cm), (2.6000cm, 2.6981cm), (3.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.1000cm, 1.8321cm), (4.1000cm, 1.8321cm), (3.6000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 2.6981cm), (1.1000cm, 3.5641cm), (2.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 2.6981cm), (2.6000cm, 2.6981cm), (2.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 2.6981cm), (2.1000cm, 3.5641cm), (3.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 2.6981cm), (3.6000cm, 2.6981cm), (3.1000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 3.5641cm), (3.1000cm, 3.5641cm), (2.6000cm, 4.4301cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(9) = 31$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[31 cells, 1838 fixed $n$-iamonds, bbox 6 x 10, solved in 4.9s within the search rectangle]
]
#v(0.2em)
#align(center)[
#box(width: 5.20cm, height: 5.40cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 0.1000cm), (1.1000cm, 0.9660cm), (2.1000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.6000cm, 0.1000cm), (3.1000cm, 0.9660cm), (4.1000cm, 0.9660cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.1000cm, 0.9660cm), (1.1000cm, 0.9660cm), (0.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.9660cm), (0.6000cm, 1.8321cm), (1.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 0.9660cm), (2.1000cm, 0.9660cm), (1.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 0.9660cm), (1.6000cm, 1.8321cm), (2.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 0.9660cm), (3.1000cm, 0.9660cm), (2.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.1000cm, 0.9660cm), (2.6000cm, 1.8321cm), (3.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.1000cm, 0.9660cm), (4.1000cm, 0.9660cm), (3.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (4.1000cm, 0.9660cm), (3.6000cm, 1.8321cm), (4.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (4.1000cm, 0.9660cm), (5.1000cm, 0.9660cm), (4.6000cm, 1.8321cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 1.8321cm), (0.1000cm, 2.6981cm), (1.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (0.6000cm, 1.8321cm), (1.6000cm, 1.8321cm), (1.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 1.8321cm), (1.1000cm, 2.6981cm), (2.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 1.8321cm), (2.6000cm, 1.8321cm), (2.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 1.8321cm), (2.1000cm, 2.6981cm), (3.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 1.8321cm), (3.6000cm, 1.8321cm), (3.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.6000cm, 1.8321cm), (3.1000cm, 2.6981cm), (4.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.6000cm, 1.8321cm), (4.6000cm, 1.8321cm), (4.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (4.6000cm, 1.8321cm), (4.1000cm, 2.6981cm), (5.1000cm, 2.6981cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.1000cm, 2.6981cm), (2.1000cm, 2.6981cm), (1.6000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 2.6981cm), (1.6000cm, 3.5641cm), (2.6000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 2.6981cm), (3.1000cm, 2.6981cm), (2.6000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.1000cm, 2.6981cm), (2.6000cm, 3.5641cm), (3.6000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.1000cm, 2.6981cm), (4.1000cm, 2.6981cm), (3.6000cm, 3.5641cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 3.5641cm), (1.1000cm, 4.4301cm), (2.1000cm, 4.4301cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.6000cm, 3.5641cm), (2.6000cm, 3.5641cm), (2.1000cm, 4.4301cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 3.5641cm), (2.1000cm, 4.4301cm), (3.1000cm, 4.4301cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.6000cm, 3.5641cm), (3.6000cm, 3.5641cm), (3.1000cm, 4.4301cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.6000cm, 3.5641cm), (3.1000cm, 4.4301cm), (4.1000cm, 4.4301cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1000cm, 4.4301cm), (3.1000cm, 4.4301cm), (2.6000cm, 5.2962cm))]
  ]
]
]
]
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)