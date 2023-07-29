export const getButtons = ({ action }) => [
  {
    onClick: () => {
      action((prev) => ({ ...prev, category: true }));
    },
    color: "warning",
    size: "small",
    text: "Categorías",
  },
  {
    onClick: () => {
      action((prev) => ({ ...prev, prices: true }));
    },
    color: "success",
    size: "small",
    text: "Actualizar Precios",
  },
  {
    onClick: () => {
      action((prev) => ({ ...prev, add: true }));
    },
    size: "small",
    text: "Agregar Producto",
  },
];

export const getModalObject = ({ open, action, key, fetchInventory }) => {
  return {
    open: open[key],
    onClose: () => action((prev) => ({ ...prev, [key]: false })),
    fetchInventory,
  };
};
